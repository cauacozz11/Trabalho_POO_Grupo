
# CLASSE BASE: ITENS DA BIBLIOTECA

# Essa classe representa qualquer item da biblioteca (livro ou revista)
# e contém os atributos e métodos em comum.
class ItensBiblioteca:
    def __init__(self, categoria, titulo, editora):
        # Atributos básicos de um item
        self.__categoria = categoria
        self.__titulo = titulo
        self.__editora = editora
        # Define que o item começa como disponível para aluguel
        self.__disponivel = True


    # PROPRIEDADE: CATEGORIA
    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, valor):
        # isinstance() verifica o tipo da variável
        # str.strip() remove espaços extras
        if isinstance(valor, str) and valor.replace(" ", "").isalpha():
            self.__categoria = valor
        else:
            raise ValueError("Categoria deve ser uma string não vazia")

   
    # PROPRIEDADE: TÍTULO
    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, valor):
        if isinstance(valor, str) and valor.strip():
            self.__titulo = valor
        else:
            raise ValueError("Título deve ser uma string não vazia")


    # PROPRIEDADE: EDITORA
    @property
    def editora(self):
        return self.__editora

    @editora.setter
    def editora(self, valor):
        if isinstance(valor, str) and valor.strip():
            self.__editora = valor
        else:
            raise ValueError("Editora deve ser uma string não vazia")

   
    # PROPRIEDADE: DISPONIBILIDADE
    @property
    def disponivel(self):
        # Retorna True ou False (se o item está disponível)
        return self.__disponivel

 
    # MÉTODOS DE STATUS (emprestar/devolver)
    def status_emprestar(self):
        # Verifica se o item está disponível e o marca como alugado
        if self.__disponivel:
            self.__disponivel = False
            return True
        return False

    def status_devolver(self):
        # Marca o item novamente como disponível
        self.__disponivel = True

   
    # MÉTODO: MOSTRAR INFORMAÇÕES DO ITEM
    def mostrar_item(self):
        status = "Disponível" if self.__disponivel else "Indisponível"
        return f"Categoria: {self.__categoria} | Título: {self.__titulo} | Editora: {self.__editora} | Status: {status}"


# CLASSE: LIVRO
# Herda da classe ItensBiblioteca e adiciona o autor.
class Livro(ItensBiblioteca):
    def __init__(self, categoria, titulo, editora, autor):
        # Chama o construtor da classe base (ItensBiblioteca)
        super().__init__(categoria, titulo, editora)
        self.__autor = autor  # Adiciona o autor do livro

    @property
    def autor(self):
        return self.__autor

    @autor.setter
    def autor(self, valor):
        # Valida se o nome do autor é uma string válida
        if isinstance(valor, str) and valor.replace(" ", "").isalpha():
            self.__autor = valor
        else:
            raise ValueError("Autor deve ser uma string não vazia")

 
    # MÉTODO: MOSTRAR INFORMAÇÕES DO LIVRO
    def mostrar_informacoes(self):
        # super() chama o método mostrar_item() da classe base
        return f"INFORMAÇÕES LIVRO\n{super().mostrar_item()} | Autor: {self.__autor}"



# CLASSE: REVISTA
# Herda de ItensBiblioteca e adiciona a edição.
class Revista(ItensBiblioteca):
    def __init__(self, categoria, titulo, editora, edicao):
        super().__init__(categoria, titulo, editora)
        self.__edicao = edicao  # Número da edição da revista

    @property
    def edicao(self):
        return self.__edicao

    @edicao.setter
    def edicao(self, valor):
        # isinstance() verifica o tipo e garante que é inteiro positivo
        if isinstance(valor, int) and valor > 0:
            self.__edicao = valor
        else:
            raise ValueError("Edição deve ser um número inteiro positivo")

   
    # MÉTODO: MOSTRAR INFORMAÇÕES DA REVISTA
    def mostrar_informacoes(self):
        return f"INFORMAÇÕES REVISTA\n{super().mostrar_item()} | Edição: {self.__edicao}"
