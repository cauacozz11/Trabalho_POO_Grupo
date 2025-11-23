from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from datetime import datetime, timedelta

# Importa o db e os Modelos do Flask-SQLAlchemy
from database import db, Cliente, Material, Emprestimo 

bp = Blueprint('main', __name__)

# Configuração de prazo padrão para o empréstimo (ex: 7 dias)
PRAZO_EMPRESTIMO_DIAS = 7


# --- Rotas de Visualização (Home, Itens) ---

@bp.route('/')
def index():
    """Página inicial."""
    return render_template('index.html')

@bp.route('/itens')
def listar_itens():
    """Lista todos os livros e revistas no acervo."""
    materiais = db.session.execute(db.select(Material)).scalars().all()

    livros = [m for m in materiais if m.tipo == 'Livro']
    revistas = [m for m in materiais if m.tipo == 'Revista']

    return render_template('itens.html', livros=livros, revistas=revistas)


# --- Rotas de Cadastro (Novo) ---

@bp.route('/cadastro/<tipo>', methods=['GET'])
def formulario_cadastro(tipo):
    """Exibe o formulário de cadastro genérico."""
    tipos_validos = ['livro', 'revista', 'cliente']
    
    if tipo not in tipos_validos:
        return redirect(url_for('main.index'))
    
    return render_template('cadastro.html', tipo=tipo)


@bp.route('/cadastro/processar', methods=['POST'])
def processar_cadastro():
    """Processa o formulário de cadastro recebido."""
    
    tipo = request.form.get('tipo')
    
    try:
        # =========================================
        # LÓGICA PARA CLIENTES
        # =========================================
        if tipo == 'cliente':
            if not request.form.get('cpf') or not request.form.get('nome'):
                 flash("Nome e CPF são obrigatórios!", 'error')
                 return redirect(url_for('main.formulario_cadastro', tipo='cliente'))

            cpf_existente = db.session.execute(
                db.select(Cliente).filter_by(cpf=request.form.get('cpf'))
            ).scalar_one_or_none()
            
            if cpf_existente:
                flash("Erro: CPF já cadastrado.", 'error')
                return redirect(url_for('main.formulario_cadastro', tipo='cliente'))

            novo_cliente = Cliente(
                nome=request.form.get('nome'),
                cpf=request.form.get('cpf'),
                telefone=request.form.get('telefone')
            )
            db.session.add(novo_cliente)
            
            # MENSAGEM DE SUCESSO REMOVIDA (Cadastro)

        # =========================================
        # LÓGICA PARA LIVROS E REVISTAS
        # =========================================
        elif tipo in ['livro', 'revista']:
            titulo = request.form.get('titulo')
            categoria = request.form.get('categoria')
            editora = request.form.get('editora')
            
            if not titulo or not editora:
                flash("Título e Editora são obrigatórios!", 'error')
                return redirect(url_for('main.formulario_cadastro', tipo=tipo))

            if tipo == 'livro':
                novo_material = Material(
                    tipo="Livro",
                    titulo=titulo,
                    categoria=categoria,
                    editora=editora,
                    autor=request.form.get('autor')
                )
                
            else: # Se for revista
                edicao_val = request.form.get('edicao')
                if not edicao_val:
                    edicao_val = 1
                
                novo_material = Material(
                    tipo="Revista",
                    titulo=titulo,
                    categoria=categoria,
                    editora=editora,
                    edicao=int(edicao_val)
                )
            
            db.session.add(novo_material)
            
            # MENSAGEM DE SUCESSO REMOVIDA (Cadastro)
            
        # Confirma a gravação no banco de dados
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao cadastrar: {e}", 'error')

    return redirect(url_for('main.index'))


# --- Rotas de Locação ---

@bp.route('/locacao')
def locacao():
    """Lista itens disponíveis para locação (Passo 1)."""
    
    materiais_disponiveis = db.session.execute(
        db.select(Material).filter_by(disponivel=True)
    ).scalars().all()
    
    livros = [m for m in materiais_disponiveis if m.tipo == 'Livro']
    revistas = [m for m in materiais_disponiveis if m.tipo == 'Revista']

    return render_template('locacao.html', livros=livros, revistas=revistas)


@bp.route('/locacao/selecionar/<int:material_id>')
def locacao_selecionar_cliente(material_id):
    """Exibe a lista de clientes após um item ser selecionado (Passo 2)."""
    
    item = db.session.get(Material, material_id)
    clientes = db.session.execute(db.select(Cliente)).scalars().all()

    if not item:
        flash("Item não encontrado ou indisponível.", 'error')
        return redirect(url_for('main.locacao'))
        
    return render_template(
        'locacao_selecionar_cliente.html',
        item=item,
        clientes=clientes
    )


@bp.route('/locacao/finalizar', methods=['POST'])
def finalizar_locacao():
    """Efetiva o empréstimo do item para o cliente (Passo 3)."""
    
    cliente_id = request.form.get('cliente_id')
    material_id = request.form.get('material_id') 

    try:
        item = db.session.get(Material, material_id)
        cliente = db.session.get(Cliente, cliente_id)
        
        if not item or not cliente or not item.disponivel:
            flash('Erro na locação: Item não encontrado ou indisponível.', 'error')
            return redirect(url_for('main.locacao'))

        item.disponivel = False
        
        data_prazo = datetime.now() + timedelta(days=PRAZO_EMPRESTIMO_DIAS)
        novo_emprestimo = Emprestimo(
            cliente_id=cliente.id, 
            material_id=item.id, 
            data_prazo=data_prazo,
            status="ABERTO"
        )
        
        db.session.add(novo_emprestimo)
        db.session.commit()
        
        # MENSAGEM DE SUCESSO REMOVIDA AQUI (LOCAÇÃO)
        # flash(f'Sucesso! "{item.titulo}" alugado para {cliente.nome}.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao finalizar a locação: {e}', 'error')
        
    return redirect(url_for('main.index'))


# --- Rotas de Devolução ---

@bp.route('/devolucao')
def devolucao():
    """Lista todos os clientes com itens alugados."""
    
    emprestimos_abertos = db.session.execute(
        db.select(Emprestimo)
          .filter_by(status="ABERTO")
          .order_by(Emprestimo.cliente_id)
    ).scalars().all()
    
    clientes_com_aluguel = []
    clientes_map = {} 

    for emp in emprestimos_abertos:
        cliente_id = emp.cliente.id
        
        if cliente_id not in clientes_map:
            cliente_data = {
                'id_cliente': cliente_id,
                'nome': emp.cliente.nome,
                'itens_alugados': []
            }
            clientes_map[cliente_id] = cliente_data
            clientes_com_aluguel.append(cliente_data)

        clientes_map[cliente_id]['itens_alugados'].append({
            'titulo': emp.material.titulo,
            'categoria': emp.material.categoria,
            'editora': emp.material.editora,
            'emprestimo_id': emp.id 
        })
    
    return render_template('devolucao.html', clientes=clientes_com_aluguel)


@bp.route('/devolucao/finalizar', methods=['POST'])
def finalizar_devolucao():
    """Processa a devolução de um item."""
    
    emprestimo_id = request.form.get('emprestimo_id') 
    
    try:
        emprestimo = db.session.get(Emprestimo, emprestimo_id)
        
        if not emprestimo:
            flash('Erro: Empréstimo não encontrado.', 'error')
            return redirect(url_for('main.devolucao'))
            
        emprestimo.data_devolucao = datetime.now()
        emprestimo.status = "DEVOLVIDO"
        
        emprestimo.material.disponivel = True
        
        db.session.commit()
        
        # MENSAGEM DE SUCESSO REMOVIDA AQUI (DEVOLUÇÃO)
        # flash(f'Devolvido com sucesso: "{emprestimo.material.titulo}".', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao finalizar a devolução: {e}', 'error')
        
    return redirect(url_for('main.devolucao'))