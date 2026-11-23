from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import Agendamento, Aluno, Instrutor, Veiculo
from app import db

agendamentos_bp = Blueprint('agendamentos', __name__, url_prefix='/agendamentos')


def _get_form_data():
    return {
        'alunos': Aluno.query.filter_by(ativo=True).order_by(Aluno.nome).all(),
        'instrutores': Instrutor.query.filter_by(ativo=True).order_by(Instrutor.nome).all(),
        'veiculos': Veiculo.query.filter_by(situacao='ativo').all(),
    }


@agendamentos_bp.route('/')
@login_required
def lista():
    agendamentos = Agendamento.query.order_by(Agendamento.data_hora.desc()).all()
    return render_template('agendamentos/lista.html', agendamentos=agendamentos)


@agendamentos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form_data = _get_form_data()

    if request.method == 'POST':
        try:
            data_hora = datetime.strptime(request.form.get('data_hora'), '%Y-%m-%dT%H:%M')
            agendamento = Agendamento(
                aluno_id=request.form.get('aluno_id'),
                instrutor_id=request.form.get('instrutor_id'),
                veiculo_id=request.form.get('veiculo_id') or None,
                tipo=request.form.get('tipo'),
                data_hora=data_hora,
                status=request.form.get('status', 'agendado'),
                observacoes=request.form.get('observacoes') or None,
            )
            db.session.add(agendamento)
            db.session.commit()
            flash('Agendamento criado com sucesso!', 'success')
            return redirect(url_for('agendamentos.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    return render_template('agendamentos/form.html', agendamento=None, **form_data)


@agendamentos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    agendamento = Agendamento.query.get_or_404(id)
    form_data = _get_form_data()

    if request.method == 'POST':
        agendamento.aluno_id = request.form.get('aluno_id')
        agendamento.instrutor_id = request.form.get('instrutor_id')
        agendamento.veiculo_id = request.form.get('veiculo_id') or None
        agendamento.tipo = request.form.get('tipo')
        agendamento.data_hora = datetime.strptime(request.form.get('data_hora'), '%Y-%m-%dT%H:%M')
        agendamento.status = request.form.get('status')
        agendamento.observacoes = request.form.get('observacoes') or None
        db.session.commit()
        flash('Agendamento atualizado!', 'success')
        return redirect(url_for('agendamentos.lista'))

    return render_template('agendamentos/form.html', agendamento=agendamento, **form_data)


@agendamentos_bp.route('/<int:id>/cancelar', methods=['POST'])
@login_required
def cancelar(id):
    agendamento = Agendamento.query.get_or_404(id)
    agendamento.status = 'cancelado'
    db.session.commit()
    flash('Agendamento cancelado.', 'warning')
    return redirect(url_for('agendamentos.lista'))
