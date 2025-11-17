import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime

# Conexão com o banco
engine = db.create_engine('sqlite:///biblioteca_completa.db') 
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False) 
    email = db.Column(db.String(100)) # Opcional, já que seu input não pedia
    telefone = db.Column(db.String(20))
    data_cadastro = db.Column(db.DateTime, default=datetime.now)
    
    # Relacionamento
    emprestimos = relationship("Emprestimo", back_populates="cliente")

    def __repr__(self):
        return f"{self.nome} (CPF: {self.cpf})"

class Material(Base):
    __tablename__ = 'acervo'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))   # 'Livro' ou 'Revista'
    titulo = db.Column(db.String(200), nullable=False)
    
    # Campos trazidos das suas classes antigas
    categoria = db.Column(db.String(100)) 
    editora = db.Column(db.String(100))
    autor = db.Column(db.String(100)) # Apenas para Livros
    edicao = db.Column(db.Integer)    # Apenas para Revistas
    
    disponivel = db.Column(db.Boolean, default=True) 
    
    emprestimos = relationship("Emprestimo", back_populates="material")

    def __repr__(self):
        return f"[{self.tipo}] {self.titulo}"

class Emprestimo(Base):
    __tablename__ = 'emprestimos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('acervo.id'))
    
    data_saida = db.Column(db.DateTime, default=datetime.now)
    data_prazo = db.Column(db.DateTime) 
    data_devolucao = db.Column(db.DateTime, nullable=True) 
    status = db.Column(db.String(20), default="ABERTO") 
    
    cliente = relationship("Cliente", back_populates="emprestimos")
    material = relationship("Material", back_populates="emprestimos")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Banco de dados atualizado com sucesso!")