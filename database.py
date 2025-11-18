# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instância que será inicializada no __init__.py
db = SQLAlchemy()

# As classes de modelo (tables)
class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False) 
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    data_cadastro = db.Column(db.DateTime, default=datetime.now)
    
    # Relacionamento
    emprestimos = db.relationship("Emprestimo", back_populates="cliente")

    def __repr__(self):
        return f"Cliente(id={self.id}, nome='{self.nome}')"

class Material(db.Model):
    __tablename__ = 'acervo'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))   # 'Livro' ou 'Revista'
    titulo = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100)) 
    editora = db.Column(db.String(100))
    autor = db.Column(db.String(100)) 
    edicao = db.Column(db.Integer)    
    disponivel = db.Column(db.Boolean, default=True) 
    
    emprestimos = db.relationship("Emprestimo", back_populates="material")

    def __repr__(self):
        return f"Material(id={self.id}, titulo='{self.titulo}')"

class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('acervo.id'))
    
    data_saida = db.Column(db.DateTime, default=datetime.now)
    data_prazo = db.Column(db.DateTime) 
    # Usei data_devolucao para evitar confusão com 'data_retorno_prevista' do seu routes.py
    data_devolucao = db.Column(db.DateTime, nullable=True) 
    status = db.Column(db.String(20), default="ABERTO") 
    
    cliente = db.relationship("Cliente", back_populates="emprestimos")
    material = db.relationship("Material", back_populates="emprestimos")