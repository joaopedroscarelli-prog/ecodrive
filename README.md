# EcoDrive — Sistema de Gestão de Autoescola

Sistema web completo para gestão de autoescola, desenvolvido em Python com Flask.
Projeto acadêmico — USJT Mooca.

## Funcionalidades

- Dashboard com estatísticas em tempo real
- Gestão de Alunos (cadastro, edição, busca, desativação)
- Gestão de Instrutores
- Gestão de Veículos (frota com controle de situação e vistoria)
- Agendamentos de aulas teóricas e práticas
- Controle de Presença por agendamento
- Controle de Pagamentos (mensalidades, taxas)
- Autenticação com login seguro (hash de senha)

## Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.10+ / Flask 3.0 |
| Banco de Dados | SQLite + Flask-SQLAlchemy |
| Autenticação | Flask-Login + Werkzeug |
| Frontend | Bootstrap 5.3 + Bootstrap Icons |
| Arquitetura | MVC com Blueprints |

## Como executar

**1. Clone o repositório**
```bash
git clone https://github.com/SEU-USUARIO/ecodrive.git
cd ecodrive
```

**2. Crie e ative o ambiente virtual**
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux / Mac:
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Execute**
```bash
python run.py
```

**5. Acesse no navegador**
```
http://localhost:5000
```

## Credenciais padrão

| Campo | Valor |
|-------|-------|
| E-mail | admin@ecodrive.com |
| Senha | admin123 |

O banco de dados SQLite (`ecodrive.db`) é criado automaticamente na primeira execução.

## Estrutura do projeto

```
ecodrive/
├── run.py               # Ponto de entrada
├── config.py            # Configurações
├── requirements.txt
├── README.md
└── app/
    ├── __init__.py      # App factory + registro de blueprints
    ├── models.py        # Models (Usuario, Aluno, Instrutor, Veiculo, Agendamento, Presenca, Pagamento)
    ├── routes/          # Controllers (blueprints)
    │   ├── auth.py
    │   ├── dashboard.py
    │   ├── alunos.py
    │   ├── instrutores.py
    │   ├── veiculos.py
    │   ├── agendamentos.py
    │   ├── presenca.py
    │   └── pagamentos.py
    └── templates/       # Views (Jinja2 + Bootstrap 5)
        ├── base.html
        ├── home.html
        ├── auth/
        ├── alunos/
        ├── instrutores/
        ├── veiculos/
        ├── agendamentos/
        ├── presenca/
        └── pagamentos/
```

## Autor

João Pedro Radighieri Scarelli — 824131134
USJT Mooca — Orientadora: Milkes Yone Alvarenga
