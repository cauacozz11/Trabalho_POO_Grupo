
# IMPORTAÇÕES
import random                              # Usado para gerar números aleatórios
from ClassesIntens import Livro, Revista   # Importa classes de itens da biblioteca
from ClassesPessoa import Cliente  # Importa classes de pessoas


# LISTAS GLOBAIS
# Armazenam os dados cadastrados durante o uso do sistema
clientes = []
livros = []
revistas = []


# DADOS PRÉ-CADASTRADOS (para testes)
# Objetivo: deixar o sistema pronto para testes sem precisar digitar tudo
clientes.append(Cliente("Eduardo Costa", "12345678901", "47999999999", 1))
clientes.append(Cliente("Maria Silva", "98765432100", "47988888888", 2))
clientes.append(Cliente("João Pereira", "11122233344", "47977777777", 3))
clientes.append(Cliente("Ana Souza", "22233344455", "47966666666", 4))
clientes.append(Cliente("Carlos Oliveira", "33344455566", "47955555555", 5))
clientes.append(Cliente("Fernanda Lima", "44455566677", "47944444444", 6))


# LIVROS
livros.append(Livro("Aventura", "O Senhor dos Anéis", "Martins Fontes", "J.R.R. Tolkien"))
livros.append(Livro("Terror", "It: A Coisa", "Suma", "Stephen King"))
livros.append(Livro("Fantasia", "Harry Potter e a Pedra Filosofal", "Rocco", "J.K. Rowling"))
livros.append(Livro("Drama", "A Culpa é das Estrelas", "Intrínseca", "John Green"))
livros.append(Livro("Ficção Científica", "Duna", "Aleph", "Frank Herbert"))
livros.append(Livro("Romance", "Orgulho e Preconceito", "Penguin", "Jane Austen"))


# REVISTAS
revistas.append(Revista("Tecnologia", "InfoTech", "Abril", 12))
revistas.append(Revista("Ciência", "Superinteressante", "Abril", 331))
revistas.append(Revista("Esportes", "Placar", "Abril", 45))
revistas.append(Revista("Moda", "Vogue", "Condé Nast", 202))
revistas.append(Revista("Negócios", "Exame", "Abril", 187))
revistas.append(Revista("Culinária", "Prazeres da Mesa", "Editora Três", 98))


# FUNÇÕES DE CADASTRO
def cadastrar_livro():
    """Permite o cadastro manual de um novo livro."""
    while True:
        print("\n--- Cadastro de Livro ---")

        # Categoria (aceita apenas letras e espaços)
        while True:
            categoria = input("Categoria: ")
            if categoria.replace(" ", "").isalpha():
                break
            else:
                print("A categoria deve conter apenas letras. Tente novamente.")
        while True:
            titulo = input("Título: ")
            if categoria.replace(" ", "").isalnum():
                break
            else:
                print("O título deve conter apenas letras ou números. Tente novamente.")
        
        while True:
            editora = input("Editora: ")
            if editora.replace(" ", "").isalnum():
                break
            else:
                print("A editora conter apenas letras ou números. Tente novamente.")
        
        # Autor (aceita apenas letras e espaços)
        while True:
            autor = input("Autor: ")
            if autor.replace(" ", "").isalpha():
                break
            else:
                print("O nome do autor deve conter apenas letras. Tente novamente.")
        try:
            novo_livro = Livro(categoria, titulo, editora, autor)
            livros.append(novo_livro)
            print("\nLivro cadastrado com sucesso!")
            print(novo_livro.mostrar_informacoes())

        except ValueError as e:
            print("Erro ao cadastrar livro:", e)
            continue

        opc = input("\nDeseja cadastrar outro livro? (s/n): ")
        if opc.lower() != 's':  # .lower() converte para minúsculas (aceita S ou s)
            break


def cadastrar_revista():
    """Permite cadastrar uma nova revista."""
    while True:
        print("\n--- Cadastro de Revista ---")
        #categoria = input("Categoria: ")
        #titulo = input("Título: ")
        #editora = input("Editora: ")
        
        while True:
            categoria = input("Categoria: ")
            if categoria.replace(" ", "").isalpha():
                break
            else:
                print("A categoria deve conter apenas letras. Tente novamente.")
        while True:
            titulo = input("Título: ")
            if titulo.replace(" ", "").isalnum():
                break
            else:
                print("O título deve conter apenas letras ou números. Tente novamente.") 
                       
        while True:
            editora = input("Editora: ")
            if editora.replace(" ", "").isalnum():
                break
            else:
                print("A editora deve conter apenas letras ou números. Tente novamente.")

        
         # Edição (deve ser um número inteiro positivo)
        try:
            edicao = int(input("Edição (número inteiro positivo): "))
            if edicao <= 0:
                print("A edição deve ser maior que zero.")
                continue
        except ValueError:
            print("Edição deve ser um número inteiro válido.")
            continue

        try:
            nova_revista = Revista(categoria, titulo, editora, edicao)
            revistas.append(nova_revista)
            print("\nRevista cadastrada com sucesso!")
            print(nova_revista.mostrar_informacoes())

        except ValueError as e:
            print("Erro ao cadastrar revista:", e)
            continue



        opc = input("\nDeseja cadastrar outra revista? (s/n): ")
        if opc.lower() != 's':
            break


def cadastrar_cliente():
    """Permite cadastrar um novo cliente no sistema."""
    while True:
        print("\n--- Cadastro de Cliente ---")
        nome = input("Nome: ")
        cpf = input("CPF (11 dígitos): ")
        telefone = input("Telefone (11 dígitos, DDD + número): ")

        # random.randint() → gera um ID aleatório entre 1 e 9999
        id_cliente = random.randint(1, 9999)

        try:
            novo_cliente = Cliente(nome, cpf, telefone, id_cliente)
            clientes.append(novo_cliente)
            print("\nCliente cadastrado com sucesso!")
            print(novo_cliente.mostrar_informacoes_cliente())
        except ValueError as e:
            print("Erro ao cadastrar cliente:", e)
            continue

        opc = input("\nDeseja cadastrar outro cliente? (s/n): ")
        if opc.lower() != 's':
            break


# FUNÇÕES DE LISTAGEM
def listar_clientes():
    """Mostra todos os clientes cadastrados."""
    print("\n" + "=" * 50)
    print("LISTA DE CLIENTES".center(50))
    print("=" * 50)

    if not clientes:  # Verifica se a lista está vazia
        print("Nenhum cliente cadastrado.")
    else:
        # enumerate() gera índice automático (1, 2, 3...)
        for i, c in enumerate(clientes, start=1):
            print(f"\n[{i}] -------------------------------")
            print(c.mostrar_informacoes_cliente())
            print("-" * 50)

    input("\nPressione ENTER para voltar ao menu...")


def listar_livros():
    """Mostra todos os livros cadastrados e seus status."""
    print("\n" + "=" * 50)
    print("LISTA DE LIVROS".center(50))
    print("=" * 50)

    if not livros:
        print("Nenhum livro cadastrado.")
    else:
        for i, l in enumerate(livros, start=1):
            print(f"\n[{i}] -------------------------------")
            print(l.mostrar_informacoes())
            print("-" * 50)
    input("\nPressione ENTER para voltar ao menu...")


def listar_revistas():
    """Mostra todas as revistas cadastradas e seus status."""
    print("\n" + "=" * 50)
    print("LISTA DE REVISTAS".center(50))
    print("=" * 50)

    if not revistas:
        print("Nenhuma revista cadastrada.")
    else:
        for i, r in enumerate(revistas, start=1):
            print(f"\n[{i}] -------------------------------")
            print(r.mostrar_informacoes())
            print("-" * 50)
    input("\nPressione ENTER para voltar ao menu...")


# FUNÇÃO - ALUGAR LIVRO
def alugar_livro():
    """Permite escolher cliente e livro para realizar o aluguel."""
    print("\n--- ALUGAR LIVRO ---")

    # Mostra lista de clientes
    for i, c in enumerate(clientes, start=1):
        print(f"{i}. {c.nome}")

    try:
        indice_cliente = int(input("\nEscolha o número do cliente: ")) - 1
        cliente = clientes[indice_cliente]
    except (ValueError, IndexError):
        # ValueError → digitou letra / símbolo
        # IndexError → número fora do intervalo da lista
        print("Opção inválida.")
        return

    # Mostra lista de livros
    print("\nLivros disponíveis:")
    for i, l in enumerate(livros, start=1):
        status = "Disponível" if l.disponivel else "Indisponível"
        print(f"{i}. {l.titulo} - {status}")

    try:
        indice_livro = int(input("\nEscolha o número do livro: ")) - 1
        livro = livros[indice_livro]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    if not livro.disponivel:
        print("\nEsse livro está indisponível no momento.")
        return

    # Marca o livro como emprestado e adiciona ao cliente
    livro.status_emprestar()
    cliente.alugar_item(livro)

    print(f"\nAluguel realizado com sucesso!")
    print(f"Cliente: {cliente.nome}")
    print(f"Livro: {livro.titulo}")


# FUNÇÃO - DEVOLVER LIVRO
def devolver_livro():
    """Permite devolver um livro alugado."""
    print("\n--- DEVOLVER LIVRO ---")

    # Exibe lista de clientes
    for i, c in enumerate(clientes, start=1):
        print(f"{i}. {c.nome}")

    try:
        indice_cliente = int(input("\nEscolha o número do cliente: ")) - 1
        cliente = clientes[indice_cliente]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    # Mostra os itens alugados pelo cliente
    if not cliente._Cliente__itens_alugados:
        print("Esse cliente não possui livros alugados.")
        return

    print("\nLivros alugados:")
    for i, item in enumerate(cliente._Cliente__itens_alugados, start=1):
        print(f"{i}. {item.titulo}")

    try:
        indice_item = int(input("\nEscolha o número do livro para devolver: ")) - 1
        livro = cliente._Cliente__itens_alugados[indice_item]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    # Atualiza status e remove da lista do cliente
    livro.status_devolver()
    cliente.devolver_item(livro)

    print(f"\nLivro '{livro.titulo}' devolvido com sucesso por {cliente.nome}.")


# FUNÇÕES - REVISTAS (ALUGAR E DEVOLVER)
def alugar_revista():
    """Permite alugar uma revista."""
    print("\n--- ALUGAR REVISTA ---")

    for i, c in enumerate(clientes, start=1):
        print(f"{i}. {c.nome}")

    try:
        indice_cliente = int(input("\nEscolha o número do cliente: ")) - 1
        cliente = clientes[indice_cliente]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    print("\nRevistas:")
    for i, r in enumerate(revistas, start=1):
        status = "Disponível" if r.disponivel else "Indisponível"
        print(f"{i}. {r.titulo} - {status}")

    try:
        indice_revista = int(input("\nEscolha o número da revista: ")) - 1
        revista = revistas[indice_revista]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    if not revista.disponivel:
        print("\nEssa revista está indisponível no momento.")
        return

    revista.status_emprestar()
    cliente.alugar_item(revista)

    print(f"\nAluguel realizado com sucesso!")
    print(f"Cliente: {cliente.nome}")
    print(f"Revista: {revista.titulo}")


def devolver_revista():
    """Permite devolver uma revista."""
    print("\n--- DEVOLVER REVISTA ---")

    for i, c in enumerate(clientes, start=1):
        print(f"{i}. {c.nome}")

    try:
        indice_cliente = int(input("\nEscolha o número do cliente: ")) - 1
        cliente = clientes[indice_cliente]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    if not cliente._Cliente__itens_alugados:
        print("Esse cliente não possui revistas alugadas.")
        return

    print("\nRevistas alugadas:")
    for i, item in enumerate(cliente._Cliente__itens_alugados, start=1):
        print(f"{i}. {item.titulo}")

    try:
        indice_item = int(input("\nEscolha o número da revista para devolver: ")) - 1
        revista = cliente._Cliente__itens_alugados[indice_item]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    revista.status_devolver()
    cliente.devolver_item(revista)

    print(f"\nRevista '{revista.titulo}' devolvida com sucesso por {cliente.nome}.")


# MENU PRINCIPAL
def menu_interativo():
    """Exibe o menu principal do sistema e gerencia as opções."""
    while True:
        try:
            # int() converte a entrada em número inteiro
            menu = int(input("""\n
---------------------------------                         
MENU DE OPÇÕES:

1 - Cadastrar livros
2 - Cadastrar revistas
3 - Cadastrar cliente
4 - Alugar livros
5 - Alugar revistas
6 - Devolver livros
7 - Devolver revistas
8 - Listar livros
9 - Listar revistas
10 - Listar todos os clientes
0 - Sair
---------------------------------
Digite sua opção: """))
        except ValueError:
            print("Digite apenas valores numéricos!")
            continue  # Volta ao início do loop

        # Estrutura condicional de seleção (menu)
        if menu == 0:
            print("Saindo do sistema...")
            break
        elif menu == 1:
            cadastrar_livro()
        elif menu == 2:
            cadastrar_revista()
        elif menu == 3:
            cadastrar_cliente()
        elif menu == 4:
            alugar_livro()
        elif menu == 5:
            alugar_revista()
        elif menu == 6:
            devolver_livro()
        elif menu == 7:
            devolver_revista()
        elif menu == 8:
            listar_livros()
        elif menu == 9:
            listar_revistas()
        elif menu == 10:
            listar_clientes()
        else:
            print("Opção inválida! Tente novamente.")



if __name__ == "__main__":
    menu_interativo()