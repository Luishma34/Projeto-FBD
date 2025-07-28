import panel as pn
from datetime import date
from database import db
from auth import current_user, logout_user, update_local_name
from utils import format_date_column, safe_get_value

def create_profile_page(navigate_to_main_page, navigate_to_login):
    nome_input = pn.widgets.TextInput(
        name="👤 Nome", 
        width=300, 
        placeholder="Seu nome completo"
    )
    email_input = pn.widgets.TextInput(
        name="📧 Email", 
        width=300, 
        disabled=True
    )
    data_nascimento_input = pn.widgets.DatePicker(
        name="🎂 Data de Nascimento", 
        width=300
    )
    sexo_input = pn.widgets.Select(
        name="⚧️ Sexo", 
        options=["Masculino", "Feminino", "Outro", "Prefiro não informar"], 
        width=300
    )
    senha_input = pn.widgets.PasswordInput(
        name="🔑 Nova Senha", 
        width=300, 
        placeholder="Deixe em branco para não alterar"
    )
    confirmar_senha_input = pn.widgets.PasswordInput(
        name="🔑 Confirmar Nova Senha", 
        width=300, 
        placeholder="Confirme a nova senha"
    )

    update_button = pn.widgets.Button(
        name="💾 Salvar Alterações", 
        button_type="primary", 
        width=200,
        height=40
    )
    back_button = pn.widgets.Button(
        name="🏠 Voltar", 
        button_type="warning", 
        width=120,
        height=40
    )
    confirm_delete_button = pn.widgets.Button(
        name="Excluir Conta", 
        button_type="danger",
        width=200,
        height=40
    )


    message_pane = pn.pane.HTML("", width=620)
    delete_message_pane = pn.pane.HTML("", width=620)

    def load_user_data():
        try:
            user_id = current_user.get("id")
            if not user_id:
                message_pane.object = "<div class='error-message'>Erro: Usuário não encontrado.</div>"
                return

            query = "SELECT nome, email, data_nascimento, sexo FROM usuario WHERE id_usuario = :user_id"
            results = db.execute_query(query, {"user_id": int(user_id)})
            user_data = results[0] if results else None

            if user_data:
                nome_input.value = user_data[0]
                email_input.value = user_data[1]
                data_nascimento_input.value = user_data[2]
                sexo_input.value = user_data[3]
            else:
                message_pane.object = "<div class='error-message'>Não foi possível carregar os dados do perfil.</div>"

        except Exception as e:
            message_pane.object = f"<div class='error-message'>Erro ao carregar perfil: {e}</div>"

    def update_profile(event):
        if senha_input.value != confirmar_senha_input.value:
            message_pane.object = "<div class='error-message'>As senhas não coincidem.</div>"
            return

        if senha_input.value and len(senha_input.value) < 6:
            message_pane.object = "<div class='error-message'>A nova senha deve ter no mínimo 6 caracteres.</div>"
            return

        try:
            base_query = """
            UPDATE usuario
            SET nome = :nome, data_nascimento = :data_nascimento, sexo = :sexo
            WHERE id_usuario = :user_id
            """
            params = {
                "nome": nome_input.value,
                "data_nascimento": data_nascimento_input.value,
                "sexo": sexo_input.value,
                "user_id": current_user["id"]
            }
            db.execute_query(base_query, params)

            if senha_input.value:
                password_query = "UPDATE usuario SET senha = :senha WHERE id_usuario = :user_id"
                db.execute_query(password_query, {"senha": senha_input.value, "user_id": current_user["id"]})

            message_pane.object = "<div class='success-message'>Perfil atualizado com sucesso!</div>"
            
            senha_input.value = ""
            confirmar_senha_input.value = ""
            
            update_local_name(nome_input.value)

        except Exception as e:
            message_pane.object = f"<div class='error-message'>Erro ao atualizar perfil: {e}</div>"


    def delete_account(event):
        try:
            user_id = current_user.get("id")
            query = "DELETE FROM usuario WHERE id_usuario = :user_id"
            db.execute_query(query, {"user_id": user_id})
            
            logout_user()
            navigate_to_login()

        except Exception as e:
            delete_message_pane.object = f"<div class='error-message'>Erro ao excluir a conta: {e}</div>"


    def back_to_main(event):
        navigate_to_main_page()

    update_button.on_click(update_profile)
    confirm_delete_button.on_click(delete_account)
    back_button.on_click(back_to_main)

    load_user_data()

    header = pn.pane.HTML("""
    <div class="profile-header">
        <h1 class="profile-title">👤 Meu Perfil</h1>
        <p>Edite suas informações pessoais ou gerencie sua conta.</p>
    </div>
    """)

    edit_section = pn.Column(
        pn.pane.HTML("<h2 class='section-header'>✏️ Editar Informações</h2>"),
        pn.Row(nome_input, email_input),
        pn.Row(data_nascimento_input, sexo_input),
        pn.Row(senha_input, confirmar_senha_input),
        pn.Row(update_button, confirm_delete_button),
        message_pane,
        css_classes=['section-card']
    )

    main_content = pn.Column(
        header,
        edit_section,
        css_classes=['profile-container'],
        sizing_mode='stretch_width'
    )

    return pn.Column(
        pn.Row(
            pn.Spacer(),
            back_button,
            margin=(10, 20, 0, 0)
        ),
        main_content,
        sizing_mode='stretch_width')