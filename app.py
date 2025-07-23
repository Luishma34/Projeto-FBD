import sys
import os

# Adiciona o diretório do projeto ao sys.path
# Isso garante que os módulos sejam encontrados corretamente pelo servidor Panel.
project_path = os.path.dirname(os.path.abspath(__file__))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

import panel as pn
from auth import create_test_user
from login_page import create_login_page

from main_page import create_main_page
from profile_page import create_profile_page
from humor_page import create_humor_crud_page
from alimentacao_page import create_alimentacao_crud_page
from metas_page import create_metas_crud_page

# Configuração do Panel
pn.extension('tabulator')

# Configurar tema padrão
pn.config.theme = 'default'

# Inicialização
create_test_user()

# Layout principal com configurações responsivas
main_layout = pn.Column(
    create_login_page(None),
    sizing_mode='stretch_width',
    min_height=600
)
# --- Funções de Navegação ---
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

# Após criar o layout, configurar a referência
#main_layout.objects = [create_login_page(main_layout)]
navigate_to_login()
main_layout.servable(title="🎯 Sistema de Rastreamento de Hábitos")
# Servir a aplicação com configurações melhoradas
# pn.serve(
#     main_layout, 
#     port=5008, 
#     show=True, 
#     title="🎯 Sistema de Rastreamento de Hábitos",
#     allow_websocket_origin=["localhost:5008"],
#     autoreload=False
# )