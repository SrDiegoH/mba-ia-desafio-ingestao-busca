# Desafio MBA Engenharia de Software com IA - Full Cycle

Desafio do curso 'MBA Engenharia de Software com IA' da Full Cycle

---
---

## Configuração do ambiente no Windows

1. **Criar um ambiente virtual (`venv`):** 

   ```bash
   python -m venv "$env:USERPROFILE\Workspace\MBA-AI\Atividades\venv"
   ```

2. **Ativar o ambiente virtual (`venv`):** 

   ```bash
   cd "$env:USERPROFILE\Workspace\MBA-AI\Atividades\venv\Scripts"; .\Activate.ps1 ; cd "..\..\mba-ia-desafio-ingestao-busca"
   ```
**Obs: Docs sobre python venv [aqui](https://docs.python.org/pt-br/3/library/venv.html)**

3. **Instalar as dependências a partir do `.\requirements.txt`:**

   ```bash
   pip install -r "$env:USERPROFILE\Workspace\MBA-AI\Atividades\mba-ia-desafio-ingestao-busca\requirements.txt"
   ```

**Obs: Caso seja instalada uma nova lib, gerar um novo `.\requirements.txt` com o comando:**

   ```bash
   pip freeze > "$env:USERPROFILE\Workspace\MBA-AI\Atividades\mba-ia-desafio-ingestao-busca\requirements.txt"
   ```

4. **Configurar as variáveis de ambiente:**

   - Duplique o arquivo `.\.env.example` e renomeie para `.\.env`;
   - Abra o arquivo `.\.env` e substitua na variável `DATABASE_URL` os valores `username` e `password` pelo login e senha do DB (pode ser encontrado no arquivo `.\docker-compose.yaml`);
   - Abra o arquivo `.\.env` e adicione às variáveis `GOOGLE_API_KEY` e `OPENAI_API_KEY` a  sua chave real da API (abaixo, na sessão **Criando uma API Key na OpenAI**, segue as instruções de como obtê-las)

---

## Requisitos para Execução dos Códigos

Para executar os códigos fornecidos no curso, é necessário:

1. Ter instalado:
- Python
- Docker e Docker compose

2. Criar chaves de API (API Keys) para os serviços da OpenAI e do Google Gemini e inseri-las no .env. Abaixo tem as instruções de como obtê-las.

### Criando uma API Key na OpenAI

1. **Acesse o site da OpenAI:**

   [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

2. **Faça login ou crie uma conta:**

   - Se já possuir uma conta, clique em "Login" e insira suas credenciais.
   - Caso contrário, clique em "Sign up" para criar uma nova conta.

3. **Navegue até a seção de API Keys:**

   - Após o login, clique em "API Keys" no menu lateral esquerdo.

4. **Crie uma nova API Key:**

   - Clique no botão "Create new secret key".
   - Dê um nome para a chave que a identifique facilmente.
   - Clique em "Create secret key".

5. **Copie e armazene sua API Key:**

   - A chave será exibida uma única vez. Copie-a e cole no arquivo `.\.env` na variável `OPENAI_API_KEY`.

Para mais detalhes, consulte o tutorial completo: [Como Gerar uma API Key na OpenAI?](https://hub.asimov.academy/tutorial/como-gerar-uma-api-key-na-openai/)

### Criando uma API Key no Google Gemini

1. **Acesse o Google AI Studio:**

   [https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)

2. **Faça login com sua conta Google:**

   - Utilize sua conta Google para acessar o AI Studio.

3. **Navegue até a seção de chaves de API:**

   - No painel de controle, clique em "API Keys" ou "Chaves de API".

4. **Crie uma nova API Key:**

   - Clique em "Create API Key" ou "Criar chave de API".
   - Dê um nome para a chave que a identifique facilmente.
   - A chave será gerada e exibida na tela.

5. **Copie e armazene sua API Key:**

   - Copie a chave gerada e cole no arquivo `.\.env` na variável `GOOGLE_API_KEY`.

Para mais informações, consulte a documentação oficial: [Como usar chaves da API Gemini](https://ai.google.dev/gemini-api/docs/api-key?hl=pt-BR)

**Nota:** Certifique-se de não compartilhar suas chaves de API publicamente e de armazená-las em locais seguros, pois elas concedem acesso aos serviços correspondentes.

---

## Ordem de execução

Para executar o desafio será necessário rodar primeiro:

1. Subir o banco de dados:
   ```bash
   docker compose up -d
   ```

2. Executar ingestão do PDF:
   ```bash
   python "$env:USERPROFILE\Workspace\MBA-AI\Atividades\mba-ia-desafio-ingestao-busca\src\ingest.py"
   ```

3. Rodar o chat:
   ```bash
   python "$env:USERPROFILE\Workspace\MBA-AI\Atividades\mba-ia-desafio-ingestao-busca\src\chat.py"
   ```