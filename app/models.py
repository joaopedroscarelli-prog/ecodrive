from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256))
    perfil = db.Column(db.String(20), default='aluno')  # admin, recepcionista, instrutor, aluno
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Usuario {self.email}>'


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    rg = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    categoria_cnh = db.Column(db.String(5), default='B')
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    agendamentos = db.relationship('Agendamento', backref='aluno', lazy=True)
    pagamentos = db.relationship('Pagamento', backref='aluno', lazy=True)

    def __repr__(self):
        return f'<Aluno {self.nome}>'


class Instrutor(db.Model):
    __tablename__ = 'instrutores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    matricula = db.Column(db.String(20), unique=True)
    especialidade = db.Column(db.String(20), default='ambas')  # teorica, pratica, ambas
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    agendamentos = db.relationship('Agendamento', backref='instrutor', lazy=True)
    veiculos = db.relationship('Veiculo', backref='instrutor', lazy=True)

    def __repr__(self):
        return f'<Instrutor {self.nome}>'


class Veiculo(db.Model):
    __tablename__ = 'veiculos'

    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), unique=True, nullable=False)
    modelo = db.Column(db.String(60), nullable=False)
    tipo = db.Column(db.String(20), default='carro')  # carro, moto
    situacao = db.Column(db.String(20), default='ativo')  # ativo, inativo, manutencao
    data_vistoria = db.Column(db.Date)
    instrutor_id = db.Column(db.Integer, db.ForeignKey('instrutores.id'))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    agendamentos = db.relationship('Agendamento', backref='veiculo', lazy=True)

    def __repr__(self):
        return f'<Veiculo {self.placa}>'


class Agendamento(db.Model):
    __tablename__ = 'agendamentos'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    instrutor_id = db.Column(db.Integer, db.ForeignKey('instrutores.id'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculos.id'))
    tipo = db.Column(db.String(20), nullable=False)  # teorica, pratica
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='agendado')  # agendado, confirmado, concluido, cancelado
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    presenca = db.relationship('Presenca', backref='agendamento', uselist=False, lazy=True)

    def __repr__(self):
        return f'<Agendamento {self.id}>'


class Presenca(db.Model):
    __tablename__ = 'presencas'

    id = db.Column(db.Integer, primary_key=True)
    agendamento_id = db.Column(db.Integer, db.ForeignKey('agendamentos.id'), nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    presente = db.Column(db.Boolean, default=False)
    registrado_em = db.Column(db.DateTime, default=datetime.utcnow)

    aluno = db.relationship('Aluno', backref='presencas')

    def __repr__(self):
        return f'<Presenca agendamento={self.agendamento_id} presente={self.presente}>'


class Pagamento(db.Model):
    __tablename__ = 'pagamentos'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(30), default='mensalidade')  # mensalidade, taxa_detran, outro
    status = db.Column(db.String(20), default='pendente')  # pendente, pago, vencido
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date)
    descricao = db.Column(db.String(200))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Pagamento R${self.valor} {self.status}>'
