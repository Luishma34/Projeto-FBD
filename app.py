import panel as pn
from auth import create_test_user
from login_page import create_login_page

from main_page import create_main_page
from profile_page import create_profile_page
from humor_page import create_humor_crud_page
from alimentacao_page import create_alimentacao_crud_page
from metas_page import create_metas_crud_page

pn.extension('tabulator')

pn.config.theme = 'default'

create_test_user()

main_layout = pn.Column(
    create_login_page(None),
    sizing_mode='stretch_width',
    min_height=600
)
def navigate_to_main_page():
    main_layout.objects = [create_main_page(navigate_to_login, navigate_to_profile, navigate_to_humor, navigate_to_metas, navigate_to_alimentacao)]

def navigate_to_login():
    main_layout.objects = [create_login_page(navigate_to_main_page)]

def navigate_to_profile():
    main_layout.objects = [create_profile_page(navigate_to_main_page, navigate_to_login)]

def navigate_to_humor():
    main_layout.objects = [create_humor_crud_page(navigate_to_main_page)]

def navigate_to_metas():
    main_layout.objects = [create_metas_crud_page(navigate_to_main_page)]

def navigate_to_alimentacao():
    main_layout.objects = [create_alimentacao_crud_page(navigate_to_main_page)]

navigate_to_login()
main_layout.servable(title="🎯 Sistema de Rastreamento de Hábitos")