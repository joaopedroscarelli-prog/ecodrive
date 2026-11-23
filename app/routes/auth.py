from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.ativo and usuario.check_senha(senha):
            login_user(usuario)
            flash(f'Bem-vindo, {usuario.nome}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))

        flash('E-mail ou senha inválidos.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        # In production: send reset email here
        flash('Se o e-mail estiver cadastrado, você receberá as instruções em breve.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/recuperar_senha.html')
