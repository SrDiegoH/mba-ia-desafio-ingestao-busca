from search import search_prompt

def main():
    while True:
        user_prompt = input('Faça sua pergunta:\n')

        if user_prompt.lower() == 'exit':
            print('Saindo...')
            break

        chain = search_prompt(user_prompt)

        if not chain:
            print('Não foi possível iniciar o chat. Verifique os erros de inicialização.')
            return

        print(f'\nPERGUNTA: {user_prompt}\nRESPOSTA: {chain.content}\n\nCaso queira sair, digite "exit".\n')

if __name__ == '__main__':
    main()