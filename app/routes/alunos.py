from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import Aluno
from app import db

alunos_bp = Blueprint('alunos', __name__, url_prefix='/alunos')


@alunos_bp.route('/')
@login_required
def lista():
    q = request.args.get('q', '').strip()
    query = Aluno.query
    if q:
        query = query.filter(
            Aluno.nome.ilike(f'%{q}%') | Aluno.cpf.like(f'%{q}%')
        )
    alunos = query.order_by(Aluno.nome).all()
    return render_template('alunos/lista.html', alunos=alunos, q=q)


@alunos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if request.method == 'POST':
        cpf = request.form.get('cpf', '').replace('.', '').replace('-', '')
        if Aluno.query.filter_by(cpf=cpf).first():
            flash('CPF já cadastrado no sistema.', 'danger')
            return render_template('alunos/form.html', aluno=None)

        try:
            aluno = Aluno(
                nome=request.form.get('nome'),
                cpf=cpf,
                rg=request.form.get('rg') or None,
                data_nascimento=datetime.strptime(request.form.get('data_nascimento'), '%Y-%m-%d').date(),
                email=request.form.get('email'),
                telefone=request.form.get('telefone'),
                endereco=request.form.get('endereco'),
                categoria_cnh=request.form.get('categoria_cnh', 'B'),
            )
            db.session.add(aluno)
            db.session.commit()
            flash('Aluno cadastrado com sucesso!', 'success')
            return redirect(url_for('alunos.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar aluno: {str(e)}', 'danger')

    return render_template('alunos/form.html', aluno=None)


@alunos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    aluno = Aluno.query.get_or_404(id)

    if request.method == 'POST':
        aluno.nome = request.form.get('nome')
        aluno.email = request.form.get('email')
        aluno.telefone = request.form.get('telefone')
        aluno.endereco = request.form.get('endereco')
        aluno.categoria_cnh = request.form.get('categoria_cnh')
        db.session.commit()
        flash('Dados atualizados com sucesso!', 'success')
        return redirect(url_for('alunos.lista'))

    return render_template('alunos/form.html', aluno=aluno)


@alunos_bp.route('/<int:id>/desativar', methods=['POST'])
@login_required
def desativar(id):
    aluno = Aluno.query.get_or_404(id)
    aluno.ativo = False
    db.session.commit()
    flash(f'Aluno {aluno.nome} desativado.', 'warning')
    return redirect(url_for('alunos.lista'))
