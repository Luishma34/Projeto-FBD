import panel as pn
import pandas as pd
from datetime import datetime, date
from database import db
from auth import current_user
from utils import format_date_column, safe_get_value

def create_humor_crud_page(navigate_to_main_page):
    date_filter = pn.widgets.DatePicker(
        name="📅 Filtrar por Data", 
        value=None,
        width=200
    )
    humor_filter = pn.widgets.Select(
        name="😊 Filtrar por Humor", 
        options=["Todos", "Feliz", "Triste", "Ansioso", "Calmo", "Irritado", "Animado"],
        value="Todos",
        width=200
    )
    
    date_input = pn.widgets.DatePicker(
        name="📅 Data", 
        value=date.today(),
        width=200
    )
    humor_input = pn.widgets.Select(
        name="😊 Tipo de Humor",
        options=["Feliz", "Triste", "Ansioso", "Calmo", "Irritado", "Animado"],
        width=200
    )
    observacao_input = pn.widgets.TextAreaInput(
        name="📝 Observação", 
        height=100,
        width=420,
        placeholder="Descreva como você se sente..."
    )

    search_id_input = pn.widgets.IntInput(
        name="🔍 Buscar por ID",
        value=None,
        width=200,
        placeholder="Digite o ID do registro"
    )
    
    edit_date_input = pn.widgets.DatePicker(
        name="📅 Data", 
        value=date.today(),
        width=200,
        disabled=True
    )
    edit_humor_input = pn.widgets.Select(
        name="😊 Tipo de Humor",
        options=["Feliz", "Triste", "Ansioso", "Calmo", "Irritado", "Animado"],
        width=200,
        disabled=True
    )
    edit_observacao_input = pn.widgets.TextAreaInput(
        name="📝 Observação", 
        height=100,
        width=420,
        placeholder="Descreva como você se sente...",
        disabled=True
    )
    
    add_button = pn.widgets.Button(
        name="➕ Adicionar",
        button_type="primary",
        width=120,
        height=40
    )
    back_button = pn.widgets.Button(
        name="🏠 Voltar",
        button_type="warning",
        width=120,
        height=40,
    )
    clear_button = pn.widgets.Button(
        name="🧹 Limpar",
        button_type="warning",
        width=120,
        height=40
    )
    
    search_button = pn.widgets.Button(
        name="🔍 Buscar",
        button_type="primary",
        width=120,
        height=40
    )
    edit_button = pn.widgets.Button(
        name="✏️ Editar",
        button_type="primary",
        width=120,
        height=40,
        disabled=True
    )
    delete_button = pn.widgets.Button(
        name="🗑️ Excluir",
        button_type="danger",
        width=120,
        height=40,
        disabled=True
    )
    clear_search_button = pn.widgets.Button(
        name="🧹 Limpar Busca",
        button_type="warning",
        width=120,
        height=40
    )

    message_pane = pn.pane.HTML("", width=500)
    search_message_pane = pn.pane.HTML("", width=500)

    table_pane = pn.pane.HTML("", sizing_mode="stretch_width")

    data_cache = {"df": None, "current_record": None}

    def load_humor_data():
        query = """
        SELECT id_humor, data, tipo_humor, observacao
        FROM registro_humor
        WHERE id_usuario = :user_id
        """
        params = {"user_id": current_user["id"]}

        if date_filter.value:
            query += " AND data = :date_filter"
            params["date_filter"] = date_filter.value

        if humor_filter.value != "Todos":
            query += " AND tipo_humor = :humor_filter"
            params["humor_filter"] = humor_filter.value

        query += " ORDER BY data DESC"

        try:
            df = db.fetch_dataframe(query, params)
            data_cache["df"] = df

            if not df.empty:
                df_display = df.copy()
                df_display = format_date_column(df_display, 'data')

                table_html = """
                <div style='overflow-x: auto;'>
                <table style='width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <thead>
                    <tr style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white;'>
                        <th style='padding: 15px; text-align: left; font-weight: 600;'>🆔 ID</th>
                        <th style='padding: 15px; text-align: left; font-weight: 600;'>📅 Data</th>
                        <th style='padding: 15px; text-align: left; font-weight: 600;'>😊 Humor</th>
                        <th style='padding: 15px; text-align: left; font-weight: 600;'>📝 Observação</th>
                    </tr>
                </thead>
                <tbody>
                """

                for i, row in df_display.iterrows():
                    id_value = safe_get_value(row, 'id_humor', '')
                    data_formatted = safe_get_value(row, 'data', 'Data inválida')
                    tipo_humor = safe_get_value(row, 'tipo_humor', '')
                    observacao = safe_get_value(row, 'observacao', '')

                    if len(observacao) > 45:
                        observacao_display = observacao[:42] + "..."
                    else:
                        observacao_display = observacao

                    humor_icons = {
                        'Feliz': '😊', 'Triste': '😢', 'Ansioso': '😰',
                        'Calmo': '😌', 'Irritado': '😠', 'Animado': '🤩'
                    }
                    humor_display = f"{humor_icons.get(tipo_humor, '😐')} {tipo_humor}"

                    row_color = '#f8f9fa' if i % 2 == 0 else 'white'
                    table_html += f"""
                    <tr style='background-color: {row_color}; border-bottom: 1px solid #dee2e6;'
                        onmouseover='this.style.backgroundColor="#e3f2fd"'
                        onmouseout='this.style.backgroundColor="{row_color}" '>
                        <td style='padding: 12px; border-right: 1px solid #dee2e6;'>{id_value}</td>
                        <td style='padding: 12px; border-right: 1px solid #dee2e6;'>{data_formatted}</td>
                        <td style='padding: 12px; border-right: 1px solid #dee2e6;'>{humor_display}</td>
                        <td style='padding: 12px; border-right: 1px solid #dee2e6;'>{observacao_display}</td>
                    </tr>
                    """

                table_html += """
                </tbody>
                </table>
                </div>

                """

                table_pane.object = table_html
            else:
                table_pane.object = """
                <div style='text-align: center; padding: 40px; color: #6c757d; background: #f8f9fa; border-radius: 8px; border: 2px dashed #dee2e6;'>
                    <h3>📭 Nenhum registro encontrado</h3>
                    <p>Adicione seu primeiro registro de humor para começar!</p>
                </div>
                """

        except Exception as e:
            table_pane.object = f"""
            <div style='color: #dc3545; padding: 20px; background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px;'>
                <strong>❌ Erro ao carregar dados:</strong> {str(e)}
            </div>
            """

    def search_record(event):
        if not search_id_input.value:
            search_message_pane.object = """
            <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                ⚠️ Por favor, digite um ID para buscar
            </div>
            """
            return
        
        try:
            query = """
            SELECT id_humor, data, tipo_humor, observacao
            FROM registro_humor
            WHERE id_usuario = :user_id AND id_humor = :id_humor
            """
            params = {
                "user_id": current_user["id"],
                "id_humor": search_id_input.value
            }
            
            df = db.fetch_dataframe(query, params)
            
            if not df.empty:
                record = df.iloc[0]
                data_cache["current_record"] = record
                
                edit_date_input.value = record['data']
                edit_humor_input.value = record['tipo_humor']
                edit_observacao_input.value = record['observacao'] or ""
                
                edit_date_input.disabled = False
                edit_humor_input.disabled = False
                edit_observacao_input.disabled = False
                edit_button.disabled = False
                delete_button.disabled = False
                
                search_message_pane.object = f"""
                <div style='color: #155724; background: #d4edda; border: 1px solid #c3e6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                    ✅ Registro ID {search_id_input.value} encontrado!
                </div>
                """
            else:
                clear_edit_form()
                search_message_pane.object = """
                <div style='color: #721c24; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                    ❌ Registro não encontrado
                </div>
                """
                
        except Exception as e:
            search_message_pane.object = f"""
            <div style='color: #dc3545; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ❌ Erro na busca: {str(e)}
            </div>
            """

    def clear_edit_form():
        edit_date_input.value = date.today()
        edit_humor_input.value = None
        edit_observacao_input.value = ""
        edit_date_input.disabled = True
        edit_humor_input.disabled = True
        edit_observacao_input.disabled = True
        edit_button.disabled = True
        delete_button.disabled = True
        data_cache["current_record"] = None

    def clear_search_form():
        search_id_input.value = None
        clear_edit_form()
        search_message_pane.object = """
        <div style='color: #0c5460; background: #d1ecf1; border: 1px solid #b6d4da; padding: 10px; border-radius: 5px; text-align: center;'>
            🔍 Formulário pronto para nova busca
        </div>
        """

    def update_record(event):
        if not data_cache["current_record"] is not None:
            search_message_pane.object = """
            <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                ⚠️ Nenhum registro selecionado para edição
            </div>
            """
            return
        
        if not edit_humor_input.value:
            search_message_pane.object = """
            <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                ⚠️ Por favor, selecione um tipo de humor
            </div>
            """
            return
        
        try:
            query = """
            UPDATE registro_humor 
            SET data = :data, tipo_humor = :tipo_humor, observacao = :observacao
            WHERE id_usuario = :user_id AND id_humor = :id_humor
            """
            params = {
                "user_id": current_user["id"],
                "id_humor": search_id_input.value,
                "data": edit_date_input.value,
                "tipo_humor": edit_humor_input.value,
                "observacao": edit_observacao_input.value or ""
            }
            
            db.execute_query(query, params)
            
            search_message_pane.object = """
            <div style='color: #155724; background: #d4edda; border: 1px solid #c3e6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ✅ Registro atualizado com sucesso!
            </div>
            """
            
            load_humor_data()
            clear_search_form()
            
        except Exception as e:
            search_message_pane.object = f"""
            <div style='color: #dc3545; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ❌ Erro ao atualizar registro: {str(e)}
            </div>
            """

    def delete_record(event):
        if not data_cache["current_record"] is not None:
            search_message_pane.object = """
            <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                ⚠️ Nenhum registro selecionado para exclusão
            </div>
            """
            return
        
        try:
            query = """
            DELETE FROM registro_humor 
            WHERE id_usuario = :user_id AND id_humor = :id_humor
            """
            params = {
                "user_id": current_user["id"],
                "id_humor": search_id_input.value
            }
            
            db.execute_query(query, params)
            
            search_message_pane.object = """
            <div style='color: #155724; background: #d4edda; border: 1px solid #c3e6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ✅ Registro excluído com sucesso!
            </div>
            """
            
            load_humor_data()
            clear_search_form()
            
        except Exception as e:
            search_message_pane.object = f"""
            <div style='color: #dc3545; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ❌ Erro ao excluir registro: {str(e)}
            </div>
            """

    def add_humor(event):
        if not humor_input.value:
            message_pane.object = """
            <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                ⚠️ Por favor, selecione um tipo de humor
            </div>
            """
            return
            
        try:
            query = """
            INSERT INTO registro_humor (id_usuario, data, tipo_humor, observacao)
            VALUES (:user_id, :data, :tipo_humor, :observacao)
            """
            params = {
                "user_id": current_user["id"],
                "data": date_input.value,
                "tipo_humor": humor_input.value,
                "observacao": observacao_input.value or ""
            }
            
            db.execute_query(query, params)
            
            message_pane.object = """
            <div style='color: #155724; background: #d4edda; border: 1px solid #c3e6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ✅ Registro adicionado com sucesso!
            </div>
            """
            
            clear_form()
            load_humor_data()
            
        except Exception as e:
            message_pane.object = f"""
            <div style='color: #dc3545; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ❌ Erro ao adicionar registro: {str(e)}
            </div>
            """

    def clear_form():
        date_input.value = date.today()
        humor_input.value = None
        observacao_input.value = ""
        
        add_button.visible = True

        message_pane.object = """
        <div style='color: #0c5460; background: #d1ecf1; border: 1px solid #b6d4da; padding: 10px; border-radius: 5px; text-align: center;'>
            📝 Formulário pronto para novo registro
        </div>
        """
    
    def back_to_main(event):
        navigate_to_main_page()
    
    add_button.on_click(add_humor)
    back_button.on_click(back_to_main)
    clear_button.on_click(lambda e: clear_form())
    search_button.on_click(search_record)
    edit_button.on_click(update_record)
    delete_button.on_click(delete_record)
    clear_search_button.on_click(lambda e: clear_search_form())

    def apply_filters(event):
        load_humor_data()

    date_filter.param.watch(apply_filters, 'value')
    humor_filter.param.watch(apply_filters, 'value')

    load_humor_data()


    header = pn.pane.HTML("""
    <div class="humor-header">
        <h1 class="humor-title">📊 Gerenciamento de Registros de Humor</h1>
    </div>
    """)
    
    filters_section = pn.Column(
        pn.pane.HTML("<h2 class='section-header'>🔍 Filtros</h2>"),
        pn.Row(
            date_filter, 
            humor_filter,
            align='center',
            margin=(0, 0, 10, 0)
        ),
        css_classes=['section-card']
    )
    
    records_section = pn.Column(
        pn.pane.HTML("<h2 class='section-header'>📋 Registros</h2>"),
        pn.Column(
            table_pane,
            css_classes=['data-table']
        ),
        css_classes=['section-card']
    )
    
    cadastro_tab = pn.Column(
        pn.Row(
            date_input, 
            humor_input,
            align='center',
            margin=(0, 0, 15, 0)
        ),
        pn.Row(
            pn.Spacer(),
            observacao_input,
            pn.Spacer(),
            align='center',
            margin=(0, 0, 20, 0)
        ),
        pn.Row(
            add_button,
            clear_button,
            align='center',
            margin=(0, 0, 15, 0)
        ),
        pn.Row(
            pn.Spacer(),
            message_pane,
            pn.Spacer(),
            align='center'
        )
    )
    
    edit_tab = pn.Column(
        pn.Row(
            search_id_input,
            search_button,
            align='center',
            margin=(0, 0, 15, 0)
        ),
        pn.pane.HTML("<hr style='margin: 20px 0; border: 1px solid #dee2e6;'>"),
        pn.Row(
            edit_date_input, 
            edit_humor_input,
            align='center',
            margin=(0, 0, 15, 0)
        ),
        pn.Row(
            pn.Spacer(),
            edit_observacao_input,
            pn.Spacer(),
            align='center',
            margin=(0, 0, 20, 0)
        ),
        pn.Row(
            edit_button,
            delete_button,
            clear_search_button,
            align='center',
            margin=(0, 0, 15, 0)
        ),
        pn.Row(
            pn.Spacer(),
            search_message_pane,
            pn.Spacer(),
            align='center'
        )
    )
    
    tabs = pn.Tabs(
        ("📝 Cadastro", cadastro_tab),
        ("✏️ Editar/Excluir", edit_tab),
        dynamic=True
    )
    
    form_section = pn.Column(
        pn.pane.HTML("<h2 class='section-header'>📝 Formulário de Registro</h2>"),
        tabs,
        css_classes=['section-card']
    )

    main_content = pn.Column(
        header,
        filters_section,
        records_section,
        form_section,
        css_classes=['humor-container'],
        sizing_mode='stretch_width'
    )
    
    return pn.Column(
        pn.Row(
            pn.Spacer(),
            back_button,
            margin=(10, 20, 0, 0)
        ),
        main_content,
        sizing_mode='stretch_width',
        min_height=700
    )