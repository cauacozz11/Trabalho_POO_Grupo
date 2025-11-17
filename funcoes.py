
from database import Session, Cliente, Material, Emprestimo
from datetime import datetime, timedelta
import sys

# Função auxiliar
def get_session():
    return Session()

# --- FUNÇÕES DE CADASTRO ---

def cadastrar_livro():
    session = get_session()
    while True:
        print("\n--- Cadastro de Livro ---")
        
        # Mantendo suas validações de input
        while True:
            categoria = input("Categoria: ")
            if categoria.replace(" ", "").isalpha(): break
            else: print("A categoria deve conter apenas letras.")

        while True:
            titulo = input("Título: ")
            if titulo.strip(): break # Simplifiquei para aceitar números também
            else: print("Título inválido.")
        
        while True:
            editora = input("Editora: ")
            if editora.strip(): break
            else: print("Editora inválida.")
        
        while True:
            autor = input("Autor: ")
            if autor.replace(" ", "").isalpha(): break
            else: print("Nome do autor inválido.")

        # SALVANDO NO BANCO (Aqui mudou!)
        try:
            novo_livro = Material(tipo="Livro", categoria=categoria, titulo=titulo, editora=editora, autor=autor)
            session.add(novo_livro)
            session.commit()
            print(f"\nLivro '{titulo}' salvo no banco de dados!")
        except Exception as e:
            session.rollback()
            print(f"Erro ao salvar: {e}")

        if input("\nDeseja cadastrar outro livro? (s/n): ").lower() != 's':
            break
    session.close()


def cadastrar_revista():
    session = get_session()
    while True:
        print("\n--- Cadastro de Revista ---")
        
        # Seus inputs...
        categoria = input("Categoria: ")
        titulo = input("Título: ")
        editora = input("Editora: ")
        
        try:
            edicao = int(input("Edição (número): "))
        except ValueError:
            print("Edição inválida.")
            continue

        # SALVANDO NO BANCO
        try:
            nova_revista = Material(tipo="Revista", categoria=categoria, titulo=titulo, editora=editora, edicao=edicao)
            session.add(nova_revista)
            session.commit()
            print(f"\nRevista '{titulo}' salva no banco!")
        except Exception as e:
            session.rollback()
            print(f"Erro: {e}")

        if input("\nDeseja cadastrar outra revista? (s/n): ").lower() != 's':
            break
    session.close()


def cadastrar_cliente():
    session = get_session()
    while True:
        print("\n--- Cadastro de Cliente ---")
        nome = input("Nome: ")
        cpf = input("CPF (apenas números): ")
        telefone = input("Telefone: ")

        # Verifica duplicidade no banco
        if session.query(Cliente).filter_by(cpf=cpf).first():
            print("Erro: CPF já cadastrado.")
        else:
            try:
                # SALVANDO NO BANCO
                novo_cliente = Cliente(nome=nome, cpf=cpf, telefone=telefone)
                session.add(novo_cliente)
                session.commit()
                print(f"\nCliente {nome} cadastrado!")
            except Exception as e:
                session.rollback()
                print(f"Erro: {e}")

        if input("\nDeseja cadastrar outro cliente? (s/n): ").lower() != 's':
            break
    session.close()


# --- FUNÇÕES DE LISTAGEM (Agora lendo do banco) ---

def listar_clientes():
    session = get_session()
    print("\n--- LISTA DE CLIENTES (BANCO DE DADOS) ---")
    clientes = session.query(Cliente).all()

    if not clientes:
        print("Nenhum cliente cadastrado.")
    else:
        for i, c in enumerate(clientes, start=1):
            print(f"[{i}] {c.nome} | CPF: {c.cpf} | Tel: {c.telefone}")
    
    session.close()
    input("\nPressione ENTER para voltar...")


def listar_livros():
    session = get_session()
    print("\n--- LISTA DE LIVROS ---")
    # Filtra apenas onde tipo é 'Livro'
    livros = session.query(Material).filter_by(tipo="Livro").all()

    if not livros:
        print("Nenhum livro cadastrado.")
    else:
        for i, l in enumerate(livros, start=1):
            status = "Disponível" if l.disponivel else "ALUGADO"
            print(f"[{i}] {l.titulo} (Autor: {l.autor}) - {status}")
    
    session.close()
    input("\nPressione ENTER para voltar...")


def listar_revistas():
    session = get_session()
    print("\n--- LISTA DE REVISTAS ---")
    revistas = session.query(Material).filter_by(tipo="Revista").all()

    if not revistas:
        print("Nenhuma revista cadastrada.")
    else:
        for i, r in enumerate(revistas, start=1):
            status = "Disponível" if r.disponivel else "ALUGADO"
            print(f"[{i}] {r.titulo} (Edição: {r.edicao}) - {status}")

    session.close()
    input("\nPressione ENTER para voltar...")


# --- FUNÇÕES DE ALUGUEL (Lógica do Banco) ---

def alugar_item_generico(tipo_material):
    session = get_session()
    print(f"\n--- ALUGAR {tipo_material.upper()} ---")
    
    # 1. Escolher Cliente
    clientes = session.query(Cliente).all()
    if not clientes:
        print("Sem clientes cadastrados.")
        session.close()
        return

    for i, c in enumerate(clientes, start=1):
        print(f"{i}. {c.nome}")
    
    try:
        idx = int(input("Escolha o cliente: ")) - 1
        cliente = clientes[idx]
    except:
        print("Opção inválida.")
        session.close()
        return

    # 2. Escolher Material Disponível
    materiais = session.query(Material).filter_by(tipo=tipo_material, disponivel=True).all()
    if not materiais:
        print(f"Nenhum(a) {tipo_material} disponível.")
        session.close()
        return

    for i, m in enumerate(materiais, start=1):
        print(f"{i}. {m.titulo}")

    try:
        idx_mat = int(input("Escolha o item: ")) - 1
        item = materiais[idx_mat]
        
        # 3. Efetivar Aluguel
        item.disponivel = False
        prazo = datetime.now() + timedelta(days=7)
        emp = Emprestimo(cliente_id=cliente.id, material_id=item.id, data_prazo=prazo)
        
        session.add(emp)
        session.commit()
        print(f"\nSucesso! {item.titulo} alugado para {cliente.nome}.")
        
    except Exception as e:
        print("Erro:", e)
        session.rollback()
    
    session.close()

def alugar_livro(): alugar_item_generico("Livro")
def alugar_revista(): alugar_item_generico("Revista")


# --- FUNÇÕES DE DEVOLUÇÃO ---

def devolver_item_generico(tipo_material):
    session = get_session()
    print(f"\n--- DEVOLVER {tipo_material.upper()} ---")
    
    # Busca empréstimos ABERTOS desse tipo
    emprestimos = session.query(Emprestimo).join(Material).filter(
        Emprestimo.status == "ABERTO", 
        Material.tipo == tipo_material
    ).all()

    if not emprestimos:
        print("Nada para devolver.")
        session.close()
        return

    for i, emp in enumerate(emprestimos, start=1):
        print(f"{i}. {emp.material.titulo} (Com: {emp.cliente.nome})")

    try:
        idx = int(input("Qual item devolver? ")) - 1
        emp = emprestimos[idx]
        
        emp.data_devolucao = datetime.now()
        emp.status = "DEVOLVIDO"
        emp.material.disponivel = True
        
        session.commit()
        print("Devolvido com sucesso!")
    except:
        print("Inválido.")
    
    session.close()

def devolver_livro(): devolver_item_generico("Livro")
def devolver_revista(): devolver_item_generico("Revista")

def relatorio_emprestimos():
    session = get_session()
    print("\n" + "=" * 60)
    print("RELATÓRIO DE ITENS ALUGADOS (QUEM ESTÁ COM O QUÊ)".center(60))
    print("=" * 60)

    # Busca na tabela Emprestimos tudo que está com status 'ABERTO'
    # O SQLAlchemy já traz automaticamente o .cliente e o .material vinculados
    emprestimos_ativos = session.query(Emprestimo).filter_by(status="ABERTO").all()

    if not emprestimos_ativos:
        print("Nenhum item está alugado no momento. Tudo na estante!")
    else:
        # Cabeçalho da tabela
        print(f"{'TIPO':<10} | {'TÍTULO DO ITEM':<25} | {'CLIENTE':<20}")
        print("-" * 60)

        for emp in emprestimos_ativos:
            tipo = emp.material.tipo
            titulo = emp.material.titulo
            nome_cliente = emp.cliente.nome
            
            # Formatação simples para alinhar
            print(f"{tipo:<10} | {titulo:<25} | {nome_cliente:<20}")
    
    session.close()
    input("\nPressione ENTER para voltar...")

# --- SEU MENU (Mantido Igual) ---
def menu_interativo():
    while True:
        try:
            print("""\n
---------------------------------                         
MENU DE OPÇÕES (BANCO CONECTADO):
1 - Cadastrar livros
2 - Cadastrar revistas
3 - Cadastrar cliente
4 - Alugar livros
5 - Alugar revistas
6 - Devolver livros
7 - Devolver revistas
8 - Listar livros (Acervo)
9 - Listar revistas (Acervo)
10 - Listar todos os clientes
11 - RELATÓRIO DE ALUGUÉIS (QUEM ESTÁ COM O LIVRO)
0 - Sair
---------------------------------""")
            menu = int(input("Digite sua opção: "))
        except ValueError:
            print("Digite apenas números!")
            continue

        if menu == 0: break
        elif menu == 1: cadastrar_livro()
        elif menu == 2: cadastrar_revista()
        elif menu == 3: cadastrar_cliente()
        elif menu == 4: alugar_livro()
        elif menu == 5: alugar_revista()
        elif menu == 6: devolver_livro()
        elif menu == 7: devolver_revista()
        elif menu == 8: listar_livros()
        elif menu == 9: listar_revistas()
        elif menu == 10: listar_clientes()
        elif menu == 11: relatorio_emprestimos() 
        else: print("Opção inválida!")

if __name__ == "__main__":
    # Garante que o banco existe ao iniciar
    from database import engine, Base
    Base.metadata.create_all(engine)
    menu_interativo()