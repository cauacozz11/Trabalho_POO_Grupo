from flask import Blueprint, render_template
from funcoes import livros, revistas, clientes

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/itens')
def listar_itens():
    return render_template('itens.html', livros=livros, revistas=revistas)

@bp.route('/locacao')
def locacao():
    return render_template('locacao.html', clientes=clientes, livros=livros, revistas=revistas)

@bp.route('/clientes')
def devolucao():
    return render_template('devolucao.html', clientes=clientes)
