from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
import os

# Carrega as variaveis de ambiente do ".env" que vai ser usado neste fluxo e valida se estão preenchidas
load_dotenv() 
for item in (
    'GOOGLE_EMBEDDING_MODEL',
    'GOOGLE_LLM_MODEL',
    'OPENAI_EMBEDDING_MODEL',
    'OPENAI_LLM_MODEL',
    'MODEL',
    'DATABASE_URL',
    'PG_VECTOR_COLLECTION_NAME'
):
    if not os.getenv(item):
        raise RuntimeError(f'Environment variable {item} is not set')

GOOGLE_EMBEDDING_MODEL = os.getenv('GOOGLE_EMBEDDING_MODEL')
GOOGLE_LLM_MODEL = os.getenv('GOOGLE_LLM_MODEL')
OPENAI_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL')
OPENAI_LLM_MODEL = os.getenv('OPENAI_LLM_MODEL')
MODEL = os.getenv('MODEL')
DATABASE_URL = os.getenv('DATABASE_URL')
PG_VECTOR_COLLECTION_NAME = os.getenv('PG_VECTOR_COLLECTION_NAME')

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    # Cria uma cadeia de execução comp template já predefinido no repo original e temperatura de .1
    llm_model = _return_if_is_openai_model(OPENAI_LLM_MODEL, GOOGLE_LLM_MODEL)
    chat_model = init_chat_model(model=llm_model, model_provider=MODEL, temperature=0.1)

    template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    chain = template | chat_model

    # Cria um embedding com base no modelo da Google/OpenAI, para vetorizar os dados do PDF
    embeddings = _return_if_is_openai_model(OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL), GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL))

    # Busca no DB, retornando os 10 vetores com maior similiaridade conforme descrito nos requisitos
    store = PGVector(
      embeddings=embeddings,
      collection_name=PG_VECTOR_COLLECTION_NAME,
      connection=DATABASE_URL,
      use_jsonb=True
    )
    result = store.similarity_search(question, k=10)
    context = '\n'.join(document.page_content for document in result)

    # Inicia processamento da chain passando o contexto e a pergunta do usuario
    response = chain.invoke({
        'contexto': context,
        'pergunta': question,
    })

    return response

def _return_if_is_openai_model(openai_return, not_openai_return):
    return openai_return if MODEL == 'opeanai' else not_openai_return