from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import Veiculo, Instrutor
from app import db

veiculos_bp = Blueprint('veiculos', __name__, url_prefix='/veiculos')


@veiculos_bp.route('/')
@login_required
def lista():
    veiculos = Veiculo.query.order_by(Veiculo.modelo).all()
    return render_template('veiculos/lista.html', veiculos=veiculos)


@veiculos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    instrutores = Instrutor.query.filter_by(ativo=True).order_by(Instrutor.nome).all()

    if request.method == 'POST':
        placa = request.form.get('placa', '').upper().strip()
        if Veiculo.query.filter_by(placa=placa).first():
            flash('Placa já cadastrada.', 'danger')
            return render_template('veiculos/form.html', veiculo=None, instrutores=instrutores)

        data_vistoria_str = request.form.get('data_vistoria')
        data_vistoria = datetime.strptime(data_vistoria_str, '%Y-%m-%d').date() if data_vistoria_str else None

        try:
            veiculo = Veiculo(
                placa=placa,
                modelo=request.form.get('modelo'),
                tipo=request.form.get('tipo', 'carro'),
                situacao=request.form.get('situacao', 'ativo'),
                data_vistoria=data_vistoria,
                instrutor_id=request.form.get('instrutor_id') or None,
            )
            db.session.add(veiculo)
            db.session.commit()
            flash('Veículo cadastrado!', 'success')
            return redirect(url_for('veiculos.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    return render_template('veiculos/form.html', veiculo=None, instrutores=instrutores)


@veiculos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    veiculo = Veiculo.query.get_or_404(id)
    instrutores = Instrutor.query.filter_by(ativo=True).order_by(Instrutor.nome).all()

    if request.method == 'POST':
        veiculo.modelo = request.form.get('modelo')
        veiculo.tipo = request.form.get('tipo')
        veiculo.situacao = request.form.get('situacao')
        veiculo.instrutor_id = request.form.get('instrutor_id') or None
        data_vistoria_str = request.form.get('data_vistoria')
        veiculo.data_vistoria = datetime.strptime(data_vistoria_str, '%Y-%m-%d').date() if data_vistoria_str else None
        db.session.commit()
        flash('Veículo atualizado!', 'success')
        return redirect(url_for('veiculos.lista'))

    return render_template('veiculos/form.html', veiculo=veiculo, instrutores=instrutores)


@veiculos_bp.route('/<int:id>/remover', methods=['POST'])
@login_required
def remover(id):
    veiculo = Veiculo.query.get_or_404(id)
    if veiculo.agendamentos:
        flash('Veículo possui agendamentos e não pode ser removido. Altere a situação para Inativo.', 'danger')
        return redirect(url_for('veiculos.lista'))
    db.session.delete(veiculo)
    db.session.commit()
    flash('Veículo removido.', 'info')
    return redirect(url_for('veiculos.lista'))
