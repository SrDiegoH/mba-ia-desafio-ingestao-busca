from search import search_prompt

def main():
    while True:
        user_prompt = input('Faça sua pergunta ou digite "exit" para sair?\n')

        if user_prompt.lower() == 'exit':
            print('Saindo...')
            break

        chain = search_prompt(user_prompt)

        if not chain:
            print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
            return

        print(f'Sua Pergunta: {user_prompt}\nResposta: {chain.content}\n\n')

if __name__ == "__main__":
    main()