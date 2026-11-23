from datetime import datetime, date
from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Aluno, Instrutor, Veiculo, Agendamento, Pagamento

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    hoje_start = datetime.combine(date.today(), datetime.min.time())
    hoje_end = datetime.combine(date.today(), datetime.max.time())

    stats = {
        'total_alunos': Aluno.query.filter_by(ativo=True).count(),
        'total_instrutores': Instrutor.query.filter_by(ativo=True).count(),
        'total_veiculos': Veiculo.query.filter_by(situacao='ativo').count(),
        'agendamentos_hoje': Agendamento.query.filter(
            Agendamento.data_hora >= hoje_start,
            Agendamento.data_hora <= hoje_end
        ).count(),
        'pagamentos_pendentes': Pagamento.query.filter_by(status='pendente').count(),
    }

    agendamentos_recentes = (
        Agendamento.query
        .order_by(Agendamento.criado_em.desc())
        .limit(8)
        .all()
    )

    return render_template('home.html', stats=stats, agendamentos_recentes=agendamentos_recentes)
