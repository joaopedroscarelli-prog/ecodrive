from datetime import datetime, date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import Pagamento, Aluno
from app import db

pagamentos_bp = Blueprint('pagamentos', __name__, url_prefix='/pagamentos')


@pagamentos_bp.route('/')
@login_required
def lista():
    pagamentos = Pagamento.query.order_by(Pagamento.data_vencimento.desc()).all()
    return render_template('pagamentos/lista.html', pagamentos=pagamentos)


@pagamentos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    alunos = Aluno.query.filter_by(ativo=True).order_by(Aluno.nome).all()

    if request.method == 'POST':
        try:
            pagamento = Pagamento(
                aluno_id=request.form.get('aluno_id'),
                valor=float(request.form.get('valor', 0)),
                tipo=request.form.get('tipo', 'mensalidade'),
                status=request.form.get('status', 'pendente'),
                data_vencimento=datetime.strptime(request.form.get('data_vencimento'), '%Y-%m-%d').date(),
                descricao=request.form.get('descricao') or None,
            )
            db.session.add(pagamento)
            db.session.commit()
            flash('Pagamento registrado!', 'success')
            return redirect(url_for('pagamentos.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    return render_template('pagamentos/form.html', pagamento=None, alunos=alunos)


@pagamentos_bp.route('/<int:id>/confirmar', methods=['POST'])
@login_required
def confirmar(id):
    pagamento = Pagamento.query.get_or_404(id)
    pagamento.status = 'pago'
    pagamento.data_pagamento = date.today()
    db.session.commit()
    flash('Pagamento confirmado!', 'success')
    return redirect(url_for('pagamentos.lista'))


@pagamentos_bp.route('/<int:id>/remover', methods=['POST'])
@login_required
def remover(id):
    pagamento = Pagamento.query.get_or_404(id)
    db.session.delete(pagamento)
    db.session.commit()
    flash('Pagamento removido.', 'info')
    return redirect(url_for('pagamentos.lista'))
