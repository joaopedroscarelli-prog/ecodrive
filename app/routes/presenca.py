from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import Agendamento, Presenca
from app import db

presenca_bp = Blueprint('presenca', __name__, url_prefix='/presenca')


@presenca_bp.route('/')
@login_required
def lista():
    agendamentos = (
        Agendamento.query
        .filter(Agendamento.status.in_(['agendado', 'confirmado', 'concluido']))
        .order_by(Agendamento.data_hora.desc())
        .all()
    )
    return render_template('presenca/lista.html', agendamentos=agendamentos)


@presenca_bp.route('/registrar/<int:agendamento_id>', methods=['POST'])
@login_required
def registrar(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    presente = request.form.get('presente') == '1'

    if agendamento.presenca:
        agendamento.presenca.presente = presente
    else:
        presenca = Presenca(
            agendamento_id=agendamento_id,
            aluno_id=agendamento.aluno_id,
            presente=presente,
        )
        db.session.add(presenca)

    agendamento.status = 'concluido'
    db.session.commit()
    flash('Presença registrada com sucesso!', 'success')
    return redirect(url_for('presenca.lista'))
