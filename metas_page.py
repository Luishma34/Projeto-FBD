import panel as pn
from database import db
from auth import current_user
from utils import safe_get_value

def create_metas_crud_page(navigate_to_main_page):
    tipo_meta_input = pn.widgets.Select(
        name="🎯 Tipo de Meta",
        options=["Água", "Sono", "Exercícios"],
        width=200
    )
    
    horas_sono_input = pn.widgets.IntInput(
        name="⏰ Horas de Sono",
        value=8,
        start=1,
        end=24,
        width=200,
        visible=False
    )
    
    quantidade_agua_input = pn.widgets.IntInput(
        name="💧 Quantidade (ml)",
        value=2000,
        start=1,
        width=200,
        visible=False
    )
    
    duracao_exercicio_input = pn.widgets.IntInput(
        name="🏃‍♂️ Duração (min)",
        value=30,
        start=1,
        width=200,
        visible=False
    )

    search_id_input = pn.widgets.IntInput(
        name="🔍 Buscar por ID",
        value=None,
        width=200,
        placeholder="Digite o ID da meta"
    )
    
    edit_tipo_meta_input = pn.widgets.Select(
        name="🎯 Tipo de Meta",
        options=["Água", "Sono", "Exercícios"],
        width=200,
        disabled=True
    )
    
    edit_horas_sono_input = pn.widgets.IntInput(
        name="⏰ Horas de Sono",
        value=8,
        start=1,
        end=24,
        width=200,
        disabled=True,
        visible=False
    )
    
    edit_quantidade_agua_input = pn.widgets.IntInput(
        name="💧 Quantidade (ml)",
        value=2000,
        start=1,
        width=200,
        disabled=True,
        visible=False
    )
    
    edit_duracao_exercicio_input = pn.widgets.IntInput(
        name="🏃‍♂️ Duração (min)",
        value=30,
        start=1,
        width=200,
        disabled=True,
        visible=False
    )
    
    def update_fields_visibility():
        tipo = tipo_meta_input.value
        
        horas_sono_input.visible = False
        quantidade_agua_input.visible = False
        duracao_exercicio_input.visible = False
        
        if tipo == "Sono":
            horas_sono_input.visible = True
        elif tipo == "Água":
            quantidade_agua_input.visible = True
        elif tipo == "Exercícios":
            duracao_exercicio_input.visible = True
    
    def update_edit_fields_visibility():
        tipo = edit_tipo_meta_input.value
        
        edit_horas_sono_input.visible = False
        edit_quantidade_agua_input.visible = False
        edit_duracao_exercicio_input.visible = False
        
        if tipo == "Sono":
            edit_horas_sono_input.visible = True
        elif tipo == "Água":
            edit_quantidade_agua_input.visible = True
        elif tipo == "Exercícios":
            edit_duracao_exercicio_input.visible = True
    
    tipo_meta_input.param.watch(lambda event: update_fields_visibility(), 'value')
    edit_tipo_meta_input.param.watch(lambda event: update_edit_fields_visibility(), 'value')
    
    update_fields_visibility()
    
    add_button = pn.widgets.Button(
        name="➕ Adicionar",
        button_type="primary",
        width=120,
        height=40
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
        name="✏️ Atualizar",
        button_type="success",
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
        name="🧹 Limpar",
        button_type="warning",
        width=120,
        height=40
    )

    back_button = pn.widgets.Button(
        name="🏠 Voltar", 
        button_type="warning",
        width=120,
        height=40
    )
    
    def back_to_main(event):
        navigate_to_main_page()
    
    back_button.on_click(back_to_main)
    
    header = pn.pane.HTML("""
    <div class="metas-header">
        <h1 class="metas-title">🎯 Gerenciamento de Metas</h1>
    </div>
    """)
    
    table_pane = pn.pane.HTML("",sizing_mode='stretch_width')
    message_pane = pn.pane.HTML("", width=600, height=60)
    search_message_pane = pn.pane.HTML("", width=600, height=60)

    data_cache = {"df": None, "current_record": None}

    def get_meta_type_and_value(meta_id):
        try:
            query = "SELECT 1 FROM meta_agua WHERE id_meta = :meta_id"
            result = db.fetch_dataframe(query, {"meta_id": meta_id})
            if not result.empty:
                return "Água"
            
            query = "SELECT 1 FROM meta_sono WHERE id_meta = :meta_id"
            result = db.fetch_dataframe(query, {"meta_id": meta_id})
            if not result.empty:
                return "Sono"
            
            query = "SELECT 1 FROM meta_exercicio WHERE id_meta = :meta_id"
            result = db.fetch_dataframe(query, {"meta_id": meta_id})
            if not result.empty:
                return "Exercícios"
            
            return "Indefinido"
        except:
            return "Indefinido"

    def load_metas_data():
        query = """
        SELECT id_meta, valor
        FROM meta
        WHERE id_usuario = :user_id
        ORDER BY id_meta DESC
        """
        params = {"user_id": current_user["id"]}

        try:
            df = db.fetch_dataframe(query, params)
            data_cache["df"] = df

            if not df.empty:
                table_html = """
                <div style='overflow-x: auto;'>
                <table style='width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <thead>
                    <tr style='background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white;'>
                        <th style='padding: 15px; text-align: left; font-weight: 600;'>🆔 ID</th>
                        <th style='padding: 15px; text-align: left; font-weight: 600;'>🎯 Tipo</th>
                        <th style='padding: 15px; text-align: left; font-weight: 600;'>📊 Valor</th>
                    </tr>
                </thead>
                <tbody>
                """

                for i, row in df.iterrows():
                    id_value = safe_get_value(row, 'id_meta', '')
                    valor = safe_get_value(row, 'valor', '')
                    tipo = get_meta_type_and_value(id_value)
                    
                    tipo_icons = {
                        'Água': '💧', 'Sono': '💤', 'Exercícios': '🏃‍♂️'
                    }
                    tipo_display = f"{tipo_icons.get(tipo, '🎯')} {tipo}"
                    
                    if tipo == "Água":
                        valor_display = f"{valor} ml"
                    elif tipo == "Sono":
                        valor_display = f"{valor} horas"
                    elif tipo == "Exercícios":
                        valor_display = f"{valor} min"
                    else:
                        valor_display = valor

                    row_color = '#f8f9fa' if i % 2 == 0 else 'white'
                    table_html += f"""
                    <tr style='background-color: {row_color}; border-bottom: 1px solid #dee2e6;'
                        onmouseover='this.style.backgroundColor="#e3f2fd"'
                        onmouseout='this.style.backgroundColor="{row_color}" '>
                        <td style='padding: 12px; border-right: 1px solid #dee2e6;'>{id_value}</td>
                        <td style='padding: 12px; border-right: 1px solid #dee2e6;'>{tipo_display}</td>
                        <td style='padding: 12px; border-right: 1px solid #dee2e6;'>{valor_display}</td>
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
                    <h3>📭 Nenhuma meta encontrada</h3>
                    <p>Adicione sua primeira meta para começar!</p>
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
            SELECT id_meta, valor
            FROM meta 
            WHERE id_usuario = :user_id AND id_meta = :id_meta
            """
            params = {
                "user_id": current_user["id"],
                "id_meta": search_id_input.value
            }
            
            df = db.fetch_dataframe(query, params)
            
            if not df.empty:
                record = df.iloc[0]
                data_cache["current_record"] = record
                
                tipo = get_meta_type_and_value(search_id_input.value)
                valor = safe_get_value(record, 'valor', '')
                
                edit_tipo_meta_input.value = tipo
                
                if tipo == "Sono":
                    edit_horas_sono_input.value = int(valor) if valor.isdigit() else 8
                elif tipo == "Água":
                    edit_quantidade_agua_input.value = int(valor) if valor.isdigit() else 2000
                elif tipo == "Exercícios":
                    edit_duracao_exercicio_input.value = int(valor) if valor.isdigit() else 30
                
                update_edit_fields_visibility()
                
                edit_horas_sono_input.disabled = False
                edit_quantidade_agua_input.disabled = False
                edit_duracao_exercicio_input.disabled = False
                edit_button.disabled = False
                delete_button.disabled = False
                
                search_message_pane.object = """
                <div style='color: #155724; background: #d4edda; border: 1px solid #c3e6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                    ✅ Registro encontrado! Você pode editá-lo abaixo.
                </div>
                """
            else:
                search_message_pane.object = """
                <div style='color: #721c24; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                    ❌ Nenhum registro encontrado com este ID
                </div>
                """
                clear_edit_form()
                
        except Exception as e:
            search_message_pane.object = f"""
            <div style='color: #dc3545; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ❌ Erro na busca: {str(e)}
            </div>
            """

    def clear_edit_form():
        edit_tipo_meta_input.disabled = True
        edit_horas_sono_input.disabled = True
        edit_quantidade_agua_input.disabled = True
        edit_duracao_exercicio_input.disabled = True
        edit_button.disabled = True
        delete_button.disabled = True
        data_cache["current_record"] = None

    def clear_search_form():
        search_id_input.value = None
        search_message_pane.object = ""
        clear_edit_form()

    def update_record(event):
        if data_cache["current_record"] is None:
            search_message_pane.object = """
            <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                ⚠️ Nenhum registro selecionado para edição
            </div>
            """
            return
        
        tipo = edit_tipo_meta_input.value
        valor = None
        
        if tipo == "Sono":
            if not edit_horas_sono_input.value or edit_horas_sono_input.value < 1 or edit_horas_sono_input.value > 24:
                search_message_pane.object = """
                <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                    ⚠️ Por favor, digite horas de sono entre 1 e 24
                </div>
                """
                return
            valor = str(edit_horas_sono_input.value)
        elif tipo == "Água":
            if not edit_quantidade_agua_input.value or edit_quantidade_agua_input.value <= 0:
                search_message_pane.object = """
                <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                    ⚠️ Por favor, digite uma quantidade positiva de água
                </div>
                """
                return
            valor = str(edit_quantidade_agua_input.value)
        elif tipo == "Exercícios":
            if not edit_duracao_exercicio_input.value or edit_duracao_exercicio_input.value <= 0:
                search_message_pane.object = """
                <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                    ⚠️ Por favor, digite uma duração positiva de exercício
                </div>
                """
                return
            valor = str(edit_duracao_exercicio_input.value)
        
        try:
            query = """
            UPDATE meta 
            SET valor = :valor
            WHERE id_usuario = :user_id AND id_meta = :id_meta
            """
            params = {
                "user_id": current_user["id"],
                "id_meta": search_id_input.value,
                "valor": valor
            }
            
            db.execute_query(query, params)
            
            search_message_pane.object = """
            <div style='color: #155724; background: #d4edda; border: 1px solid #c3e6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ✅ Meta atualizada com sucesso!
            </div>
            """
            
            load_metas_data()
            clear_search_form()
            
        except Exception as e:
            search_message_pane.object = f"""
            <div style='color: #dc3545; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ❌ Erro ao atualizar meta: {str(e)}
            </div>
            """

    def delete_record(event):
        if data_cache["current_record"] is None:
            search_message_pane.object = """
            <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                ⚠️ Nenhuma meta selecionada para exclusão
            </div>
            """
            return
        
        try:
            query = """
            DELETE FROM meta 
            WHERE id_usuario = :user_id AND id_meta = :id_meta
            """
            params = {
                "user_id": current_user["id"],
                "id_meta": search_id_input.value
            }
            
            db.execute_query(query, params)
            
            search_message_pane.object = """
            <div style='color: #155724; background: #d4edda; border: 1px solid #c3e6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ✅ Meta excluída com sucesso!
            </div>
            """
            
            load_metas_data()
            clear_search_form()
            
        except Exception as e:
            search_message_pane.object = f"""
            <div style='color: #dc3545; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ❌ Erro ao excluir meta: {str(e)}
            </div>
            """

    def add_meta(event):
        tipo = tipo_meta_input.value
        valor = None

        if tipo == "Sono":
            if not horas_sono_input.value or horas_sono_input.value < 1 or horas_sono_input.value > 24:
                message_pane.object = """
                <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                    ⚠️ Por favor, digite horas de sono entre 1 e 24
                </div>
                """
                return
            valor = str(horas_sono_input.value)
        elif tipo == "Água":
            if not quantidade_agua_input.value or quantidade_agua_input.value <= 0:
                message_pane.object = """
                <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                    ⚠️ Por favor, digite uma quantidade positiva de água
                </div>
                """
                return
            valor = str(quantidade_agua_input.value)
        elif tipo == "Exercícios":
            if not duracao_exercicio_input.value or duracao_exercicio_input.value <= 0:
                message_pane.object = """
                <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                    ⚠️ Por favor, digite uma duração positiva de exercício
                </div>
                """
                return
            valor = str(duracao_exercicio_input.value)

        try:
            check_query = ""
            if tipo == "Água":
                check_query = """
                SELECT m.id_meta FROM meta m JOIN meta_agua ma ON m.id_meta = ma.id_meta
                WHERE m.id_usuario = :user_id
                """
            elif tipo == "Sono":
                check_query = """
                SELECT m.id_meta FROM meta m JOIN meta_sono ms ON m.id_meta = ms.id_meta
                WHERE m.id_usuario = :user_id
                """
            elif tipo == "Exercícios":
                check_query = """
                SELECT m.id_meta FROM meta m JOIN meta_exercicio me ON m.id_meta = me.id_meta
                WHERE m.id_usuario = :user_id
                """

            if check_query:
                existing_meta = db.fetch_dataframe(check_query, {"user_id": current_user["id"]})
                if not existing_meta.empty:
                    message_pane.object = f"""
                    <div style='color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; text-align: center;'>
                        ⚠️ Você já possui uma meta de {tipo}. Edite a meta existente ou exclua-a para adicionar uma nova.
                    </div>
                    """
                    return

            query = """
            INSERT INTO meta (id_usuario, valor)
            VALUES (:user_id, :valor)
            """
            params = {
                "user_id": current_user["id"],
                "valor": valor
            }

            db.execute_query(query, params)

            query_id = """
            SELECT id_meta FROM meta
            WHERE id_usuario = :user_id AND valor = :valor
            ORDER BY id_meta DESC
            LIMIT 1
            """

            result_df = db.fetch_dataframe(query_id, params)

            if not result_df.empty:
                meta_id = int(result_df.iloc[0]['id_meta'])

                if tipo == "Água":
                    query_specialized = "INSERT INTO meta_agua (id_meta) VALUES (:meta_id)"
                elif tipo == "Sono":
                    query_specialized = "INSERT INTO meta_sono (id_meta) VALUES (:meta_id)"
                elif tipo == "Exercícios":
                    query_specialized = "INSERT INTO meta_exercicio (id_meta) VALUES (:meta_id)"

                db.execute_query(query_specialized, {"meta_id": meta_id})

                message_pane.object = """
                <div style='color: #155724; background: #d4edda; border: 1px solid #c3e6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                    ✅ Meta adicionada com sucesso!
                </div>
                """
            else:
                message_pane.object = """
                <div style='color: #dc3545; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                    ❌ Erro: não foi possível obter ID da meta inserida
                </div>
                """
                return

            load_metas_data()
            clear_form()

        except Exception as e:
            message_pane.object = f"""
            <div style='color: #dc3545; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; text-align: center;'>
                ❌ Erro ao adicionar meta: {str(e)}
            </div>
            """

    def clear_form():
        horas_sono_input.value = 8
        quantidade_agua_input.value = 2000
        duracao_exercicio_input.value = 30
        message_pane.object = ""

    add_button.on_click(add_meta)
    clear_button.on_click(clear_form)
    search_button.on_click(search_record)
    edit_button.on_click(update_record)
    delete_button.on_click(delete_record)
    clear_search_button.on_click(clear_search_form)

    load_metas_data()
    
    records_section = pn.Column(
        pn.pane.HTML("<h2 class='section-header'>📋 Suas Metas</h2>"),
        table_pane,
        css_classes=['section-card']
    )
    
    cadastro_tab = pn.Column(
        pn.Row(
            tipo_meta_input,
            horas_sono_input,
            quantidade_agua_input,
            duracao_exercicio_input,
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
            edit_tipo_meta_input,
            edit_horas_sono_input,
            edit_quantidade_agua_input,
            edit_duracao_exercicio_input,
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
        pn.pane.HTML("<h2 class='section-header'>📝 Formulário de Metas</h2>"),
        tabs,
        css_classes=['section-card']
    )

    main_content = pn.Column(
        header,
        records_section,
        form_section,
        css_classes=['metas-container'],
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