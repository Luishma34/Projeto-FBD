import panel as pn
from auth import authenticate_user, current_user, hash_password
from database import db
from datetime import date
import re

def is_valid_email(email):
    """Verifica se o formato do email é válido."""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def create_login_page(navigate_to_main_page):
    """Cria a página de login e cadastro com abas."""

    # --- Componentes da Aba de Login (Já existentes) ---
    email_input = pn.widgets.TextInput(
        name="Email",
        placeholder="Digite seu email",
        width=320,
        sizing_mode="fixed"
    )
    password_input = pn.widgets.PasswordInput(
        name="Senha",
        placeholder="Digite sua senha",
        width=320,
        sizing_mode="fixed"
    )
    login_button = pn.widgets.Button(
        name="Entrar",
        button_type="primary",
        width=320,
        height=45,
        sizing_mode="fixed"
    )
    message_pane_login = pn.pane.HTML("", width=320)

    def handle_login(event):
        if authenticate_user(email_input.value, password_input.value):
            message_pane_login.object = f"""
            <div style='color: #28a745; text-align: center; padding: 10px;
                        background-color: #d4edda; border: 1px solid #c3e6cb;
                        border-radius: 5px; margin-top: 15px;'>
                ✅ Login realizado com sucesso! Bem-vindo, {current_user['nome']}
            </div>
            """
            # from main_page import create_main_page
            # main_layout.objects = [create_main_page(main_layout)]
            navigate_to_main_page()
        else:
            message_pane_login.object = """
            <div style='color: #dc3545; text-align: center; padding: 10px;
                        background-color: #f8d7da; border: 1px solid #f5c6cb;
                        border-radius: 5px; margin-top: 15px;'>
                ❌ Email ou senha incorretos
            </div>
            """

    login_button.on_click(handle_login)

    login_tab = pn.Column(
        pn.Spacer(height=10),
        email_input,
        pn.Spacer(height=15),
        password_input,
        pn.Spacer(height=25),
        login_button,
        message_pane_login,
        align='center'
    )

    # --- Componentes da Aba de Cadastro (Novos) ---
    nome_reg_input = pn.widgets.TextInput(name="Nome Completo", placeholder="Digite seu nome", width=320)
    email_reg_input = pn.widgets.TextInput(name="Email", placeholder="Digite um email válido", width=320)
    senha_reg_input = pn.widgets.PasswordInput(name="Senha", placeholder="Mínimo de 6 caracteres", width=320)
    confirm_senha_input = pn.widgets.PasswordInput(name="Confirmar Senha", placeholder="Repita a senha", width=320)
    data_nascimento_input = pn.widgets.DatePicker(name="Data de Nascimento", value=date(2000, 1, 1), end=date.today(), width=320)
    sexo_input = pn.widgets.Select(name="Sexo", options=["Masculino", "Feminino", "Outro", "Prefiro não informar"], width=320)
    
    register_button = pn.widgets.Button(name="Cadastrar", button_type="primary", width=320, height=45)
    message_pane_reg = pn.pane.HTML("", width=320)

    def handle_register(event):
        nome = nome_reg_input.value
        email = email_reg_input.value
        senha = senha_reg_input.value
        confirm_senha = confirm_senha_input.value
        data_nasc = data_nascimento_input.value
        sexo = sexo_input.value

        # Validações
        if not all([nome, email, senha, confirm_senha]):
            message_pane_reg.object = "<div style='color: #dc3545; text-align: center;'>⚠️ Preencha todos os campos obrigatórios.</div>"
            return
        if not is_valid_email(email):
            message_pane_reg.object = "<div style='color: #dc3545; text-align: center;'>📧 Email inválido.</div>"
            return
        if len(senha) < 6:
            message_pane_reg.object = "<div style='color: #dc3545; text-align: center;'>🔑 A senha deve ter no mínimo 6 caracteres.</div>"
            return
        if senha != confirm_senha:
            message_pane_reg.object = "<div style='color: #dc3545; text-align: center;'>🔑 As senhas não coincidem.</div>"
            return

        try:
            resultsExists = db.execute_query("SELECT id_usuario FROM usuario WHERE email = :email", {"email": email})
            user_dataExists = resultsExists[0] if resultsExists else None
            # Verificar se o email já existe
            if user_dataExists:
                message_pane_reg.object = "<div style='color: #dc3545; text-align: center;'>📧 Este email já está cadastrado.</div>"
                return

            # Inserir novo usuário
            query = """
            INSERT INTO usuario (nome, senha, email, data_nascimento, sexo)
            VALUES (:nome, :senha, :email, :data_nascimento, :sexo)
            """
            hashed_password = hash_password(senha)
            params = {
                'nome': nome, 'senha': hashed_password, 'email': email,
                'data_nascimento': data_nasc, 'sexo': sexo
            }
            db.execute_query(query, params)
            message_pane_reg.object = """
            <div style='color: #28a745; text-align: center;'>
                ✅ Cadastro realizado com sucesso! Você já pode fazer o login.
            </div>
            """
            # Limpar campos após sucesso
            nome_reg_input.value = ""
            email_reg_input.value = ""
            senha_reg_input.value = ""
            confirm_senha_input.value = ""

        except Exception as e:
            message_pane_reg.object = f"<div style='color: #dc3545; text-align: center;'>❌ Erro no cadastro: {e}</div>"

    register_button.on_click(handle_register)

    register_tab = pn.Column(
        pn.Spacer(height=10),
        nome_reg_input,
        email_reg_input,
        senha_reg_input,
        confirm_senha_input,
        data_nascimento_input,
        sexo_input,
        pn.Spacer(height=25),
        register_button,
        message_pane_reg,
        align='center'
    )

    # --- Estrutura Principal com Abas ---
    tabs = pn.Tabs(
        ("Entrar", login_tab),
        ("Cadastrar", register_tab),
        dynamic=True,
        width=400
    )

    login_card = pn.Column(
        pn.pane.HTML(
            "<h1 class='login-title'>🎯 Sistema de Rastreamento de Hábitos</h1>",
            margin=(0, 0, 20, 0)
        ),
        tabs,
        css_classes=['login-card'],
        align='center',
        margin=0
    )

    return pn.Column(
        pn.Spacer(),
        pn.Row(pn.Spacer(), login_card, pn.Spacer(), align='center'),
        pn.Spacer(),
        css_classes=['centered-container'],
        sizing_mode='stretch_width',
        min_height=600
    )