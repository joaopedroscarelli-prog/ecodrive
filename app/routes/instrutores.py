from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import Instrutor
from app import db

instrutores_bp = Blueprint('instrutores', __name__, url_prefix='/instrutores')


@instrutores_bp.route('/')
@login_required
def lista():
    instrutores = Instrutor.query.order_by(Instrutor.nome).all()
    return render_template('instrutores/lista.html', instrutores=instrutores)


@instrutores_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if request.method == 'POST':
        cpf = request.form.get('cpf', '').replace('.', '').replace('-', '')
        if Instrutor.query.filter_by(cpf=cpf).first():
            flash('CPF já cadastrado.', 'danger')
            return render_template('instrutores/form.html', instrutor=None)

        try:
            instrutor = Instrutor(
                nome=request.form.get('nome'),
                cpf=cpf,
                matricula=request.form.get('matricula') or None,
                especialidade=request.form.get('especialidade', 'ambas'),
                email=request.form.get('email'),
                telefone=request.form.get('telefone'),
            )
            db.session.add(instrutor)
            db.session.commit()
            flash('Instrutor cadastrado com sucesso!', 'success')
            return redirect(url_for('instrutores.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    return render_template('instrutores/form.html', instrutor=None)


@instrutores_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    instrutor = Instrutor.query.get_or_404(id)

    if request.method == 'POST':
        instrutor.nome = request.form.get('nome')
        instrutor.especialidade = request.form.get('especialidade')
        instrutor.email = request.form.get('email')
        instrutor.telefone = request.form.get('telefone')
        db.session.commit()
        flash('Instrutor atualizado!', 'success')
        return redirect(url_for('instrutores.lista'))

    return render_template('instrutores/form.html', instrutor=instrutor)


@instrutores_bp.route('/<int:id>/desativar', methods=['POST'])
@login_required
def desativar(id):
    instrutor = Instrutor.query.get_or_404(id)
    instrutor.ativo = False
    db.session.commit()
    flash(f'Instrutor {instrutor.nome} desativado.', 'warning')
    return redirect(url_for('instrutores.lista'))
