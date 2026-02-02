from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# Carrega as variaveis de ambiente do ".env" que vai ser usado neste fluxo e valida se estão preenchidas
load_dotenv() 
for item in (
    'GOOGLE_EMBEDDING_MODEL',
    'OPENAI_EMBEDDING_MODEL',
    'MODEL',
    'DATABASE_URL',
    'PG_VECTOR_COLLECTION_NAME',
    'PDF_PATH'
):
    if not os.getenv(item):
        raise RuntimeError(f'Environment variable {item} is not set')

GOOGLE_EMBEDDING_MODEL = os.getenv('GOOGLE_EMBEDDING_MODEL')
OPENAI_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL')
MODEL = os.getenv('MODEL')
DATABASE_URL = os.getenv('DATABASE_URL')
PG_VECTOR_COLLECTION_NAME = os.getenv('PG_VECTOR_COLLECTION_NAME')
PDF_PATH = os.getenv('PDF_PATH')

def ingest_pdf():
    print('Carregando PDF...')
    documents = _load_PDF()

    print('Processando PDF...')
    chunks = _split_in_chucks(documents)
    enriched_documents = _enrich(chunks)

    # Gera IDs de cada documento para salvar no DB
    ids = [ f'DOC-{i}' for i in range(len(enriched_documents)) ]

    # Cria um embedding com base no modelo da Google/OpenAI, para vetorizar os dados do PDF
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL) if MODEL == 'opeanai' else GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)

    print('Conectando ao DB...')
    store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True
    )

    print('Salvando no DB...')
    store.add_documents(documents=enriched_documents, ids=ids)

    print('Ingestão finalizada!')

# Lê o arquivo PDF
def _load_PDF():
    loader = PyPDFLoader(PDF_PATH)
    return loader.load()

# Separa o documento em partes conforme descrito nos requisitos
def _split_in_chucks(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(documents)

    # Se não conseguir separar o arquivo vai lançar um erro
    if not chunks:
        raise SystemExit(0)

    return chunks

# Cria um único documento novo enriquecido com as partes separadas
def _enrich(chunks):
    return [
        Document(
            page_content=document.page_content,
            metadata={ k: v for k, v in document.metadata.items() if v not in ('', None) }
        ) for document in chunks
    ]

# Inicia a ingestão
if __name__ == '__main__':
    ingest_pdf()