
# CLASSE BASE: PESSOA
# Essa classe é usada como base para Bibliotecário e Cliente.
# Ela contém os atributos e validações comuns a qualquer pessoa no sistema.
class Pessoa:
    def __init__(self, nome, cpf, telefone):
        # Atributos principais da pessoa
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        
        
    # PROPRIEDADE: NOME
    @property
    def nome(self):
        return self.__nome  # Retorna o valor privado do atributo nome

    @nome.setter
    def nome(self, valor):
        # isinstance() verifica o tipo da variável
        # .replace(" ", "") remove espaços para validar apenas letras
        # .isalpha() confirma se só contém letras
        if isinstance(valor, str) and valor.replace(" ", "").isalpha():
            self.__nome = valor
        else:
            raise ValueError("Nome deve conter apenas letras e espaços")
        
    # PROPRIEDADE: CPF
    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, valor):
        # .isdigit() verifica se todos os caracteres são números
        # len(valor) == 11 garante que tenha exatamente 11 dígitos
        if isinstance(valor, str) and valor.isdigit() and len(valor) == 11:
            self.__cpf = valor
        else:
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos")

    
    # PROPRIEDADE: TELEFONE
    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, valor):
        # Valida se o telefone tem apenas números e 11 dígitos (ex: DDD + número)
        if isinstance(valor, str) and valor.isdigit() and len(valor) == 11:
            self.__telefone = valor
        else:
            raise ValueError("Telefone deve conter apenas dígitos e ter 11 números")

   
    # MÉTODO: MOSTRAR INFORMAÇÕES
    def mostrar_informacoes(self):
        # Retorna uma string formatada com os dados da pessoa
        return f"Nome: {self.__nome} | CPF: {self.__cpf} | Telefone: {self.__telefone}"


# CLASSE: CLIENTE
# Herda de Pessoa e representa os usuários que alugam livros/revistas.
class Cliente(Pessoa):
    def __init__(self, nome, cpf, telefone, id_cliente):
        # Chama o construtor da classe Pessoa
        super().__init__(nome, cpf, telefone)
        self.id_cliente = id_cliente
        # Cria uma lista vazia para armazenar os itens alugados
        self.__itens_alugados = []

    
    # PROPRIEDADE: ID DO CLIENTE
    @property
    def id_cliente(self):
        return self.__id_cliente

    @id_cliente.setter
    def id_cliente(self, valor):
        # Valida se o ID é um número inteiro positivo
        if isinstance(valor, int) and valor > 0:
            self.__id_cliente = valor
        else:
            raise ValueError("ID do cliente deve ser um número inteiro positivo")

   
    # MÉTODO: MOSTRAR INFORMAÇÕES DO CLIENTE
    def mostrar_informacoes_cliente(self):
        info = f"INFORMAÇÕES CLIENTE\n{super().mostrar_informacoes()} | Cadastro: {self.__id_cliente}"
        # Exibe os itens alugados (caso existam)
        if self.__itens_alugados:
            info += "\nItens Alugados:"
            for item in self.__itens_alugados:
                info += f"\n - {item.titulo}"
        else:
            info += "\nNenhum item alugado no momento."
        return info

   
    # MÉTODO: ALUGAR ITEM
    def alugar_item(self, item):
        # Adiciona o item à lista de alugados
        self.__itens_alugados.append(item)

  
    # MÉTODO: DEVOLVER ITEM
    def devolver_item(self, item):
        # Remove o item da lista de alugados (se existir)
        if item in self.__itens_alugados:
            self.__itens_alugados.remove(item)
