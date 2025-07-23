import panel as pn
from auth import current_user


def create_main_page(navigate_to_login, navigate_to_profile, navigate_to_humor, navigate_to_metas, navigate_to_alimentacao):
    """Cria a página principal após login"""


    def logout(event):
        current_user["id"] = None
        current_user["nome"] = None
        # Importação dinâmica para evitar dependência circular
        # from login_page import create_login_page
        # main_layout.objects = [create_login_page(main_layout)]
        navigate_to_login()

    logout_button = pn.widgets.Button(
        name="🚪 Logout",
        button_type="warning",
        width=120,
        height=40
    )
    profile_button = pn.widgets.Button(
        name="👤 Perfil",
        button_type="success",
        width=120,
        height=40
    )
    
    logout_button.on_click(logout)

    humor_button = pn.widgets.Button(
        name="📊 Gerenciar Registros de Humor",
        button_type="primary",
        width=300,
        height=50,
        sizing_mode="fixed"
    )

    metas_button = pn.widgets.Button(
        name="🎯 Gerenciar Metas",
        button_type="success",
        width=300,
        height=50,
        sizing_mode="fixed"
    )

    alimentacao_button = pn.widgets.Button(
        name="🍽️ Gerenciar Alimentação",
        button_type="primary",
        width=300,
        height=50,
        sizing_mode="fixed"
    )

    def open_humor_crud(event):
        # from humor_page import create_humor_crud_page
        # humor_page = create_humor_crud_page(main_layout)
        # main_layout.objects = [humor_page]
        navigate_to_humor()

    def open_profile(event):
        # from profile_page import create_profile_page
        # profile_page = create_profile_page(main_layout)
        # main_layout.objects = [profile_page]
        navigate_to_profile()
    profile_button.on_click(open_profile)

    def open_alimentacao_crud(event):
        # from alimentacao_page import create_alimentacao_crud_page
        # alimentacao_page = create_alimentacao_crud_page(main_layout)
        # main_layout.objects = [alimentacao_page]
        navigate_to_alimentacao()
   
    def open_metas_crud(event):
        # from metas_page import create_metas_crud_page
        # metas_page = create_metas_crud_page(main_layout)
        # main_layout.objects = [metas_page]
        navigate_to_metas()

    alimentacao_button.on_click(open_alimentacao_crud)
    humor_button.on_click(open_humor_crud)
    metas_button.on_click(open_metas_crud)

    # Header de boas-vindas
    welcome_header = pn.pane.HTML(f"""
    <div class="welcome-header">
        <h1 class="welcome-title">👋 Bem-vindo, {current_user['nome']}!</h1>
        <p class="welcome-subtitle">Gerencie seus hábitos e acompanhe seu progresso pessoal</p>
    </div>
    """)

    # Card de funcionalidades disponíveis
    available_card = pn.Column(
        pn.pane.HTML("<h2 class='section-title'>🚀 Funcionalidades Disponíveis</h2>"),
        pn.Spacer(height=20),
        pn.Row(
            pn.Spacer(),
            humor_button,
            pn.Spacer(),
            align='center'
        ),
        pn.Spacer(height=15),
        pn.Row(
            pn.Spacer(),
            metas_button,
            pn.Spacer(),
            align='center'
        ),
        pn.Spacer(height=15),
        pn.Row(
            pn.Spacer(),
            alimentacao_button,
            pn.Spacer(),
            align='center'
        ),
        align='center',
    )

    # Layout principal
    main_content = pn.Column(
        welcome_header,
        available_card,
        css_classes=['main-container'],
        sizing_mode='stretch_width',
        align='center'
    )

    # Container com logout button posicionado
    return pn.Column(
        pn.Row(
            pn.Spacer(),
            logout_button,
            profile_button,
            margin=(10, 20, 0, 0)
        ),
        main_content,
        sizing_mode='stretch_width',
        min_height=600
    )