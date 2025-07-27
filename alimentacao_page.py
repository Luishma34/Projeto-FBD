import panel as pn
import pandas as pd
from datetime import datetime, date, time
from database import db
from auth import current_user
from utils import format_date_column, safe_get_value

def create_alimentacao_crud_page(navigate_to_main_page):

    tipos_refeicao = ["Café da Manhã", "Almoço", "Jantar", "Lanche", "Ceia", "Outro"]

    date_filter = pn.widgets.DatePicker(name="📅 Filtrar por Data", value=None, width=200)
    tipo_filter = pn.widgets.Select(name="🍲 Filtrar por Tipo", options=["Todos"] + tipos_refeicao, value="Todos", width=200)

    date_input = pn.widgets.DatePicker(name="📅 Data", value=date.today(), width=200)
    hora_input = pn.widgets.TextInput(name="⏰ Hora (HH:MM)", value=datetime.now().strftime("%H:%M"), width=200)
    tipo_input = pn.widgets.Select(name="🍲 Tipo de Refeição", options=tipos_refeicao, width=200)
    calorias_input = pn.widgets.IntInput(name="🔥 Calorias", value=0, start=0, width=200)
    descricao_input = pn.widgets.TextAreaInput(name="📝 Descrição (um item por linha)", height=120, width=420, placeholder="Ex: Arroz\nFeijão\nBife acebolado")

    search_id_input = pn.widgets.IntInput(name="🔍 Buscar por ID", value=None, width=200, placeholder="Digite o ID do registro")
    
    edit_date_input = pn.widgets.DatePicker(name="📅 Data", width=200, disabled=True)
    edit_hora_input = pn.widgets.TextInput(name="⏰ Hora (HH:MM)", width=200, disabled=True)
    edit_tipo_input = pn.widgets.Select(name="🍲 Tipo de Refeição", options=tipos_refeicao, width=200, disabled=True)
    edit_calorias_input = pn.widgets.IntInput(name="🔥 Calorias", start=0, width=200, disabled=True)
    edit_descricao_input = pn.widgets.TextAreaInput(name="📝 Descrição", height=120, width=420, disabled=True)

    add_button = pn.widgets.Button(name="➕ Adicionar", button_type="primary", width=120, height=40)
    back_button = pn.widgets.Button(name="🏠 Voltar", button_type="warning", width=120, height=40)
    clear_button = pn.widgets.Button(name="🧹 Limpar", button_type="warning", width=120, height=40)
    search_button = pn.widgets.Button(name="🔍 Buscar", button_type="primary", width=120, height=40)
    edit_button = pn.widgets.Button(name="✏️ Editar", button_type="primary", width=120, height=40, disabled=True)
    delete_button = pn.widgets.Button(name="🗑️ Excluir", button_type="danger", width=120, height=40, disabled=True)
    clear_search_button = pn.widgets.Button(name="🧹 Limpar Busca", button_type="warning", width=120, height=40)

    message_pane = pn.pane.HTML("", width=500)
    search_message_pane = pn.pane.HTML("", width=500)

    table_pane = pn.pane.HTML("", sizing_mode="stretch_width")
    data_cache = {"df": None, "current_record": None}

    def load_alimentacao_data():
        query = """
        SELECT 
            ra.id_registro_alimentacao, 
            ra.data, 
            ra.hora, 
            ra.tipo, 
            ra.calorias,
            STRING_AGG(rad.descricao, ', ') AS descricao
        FROM registro_alimentacao ra
        LEFT JOIN registro_alimentacao_descricao rad 
            ON ra.id_registro_alimentacao = rad.id_registro_alimentacao
        WHERE ra.id_usuario = :user_id
        """
        params = {"user_id": current_user["id"]}

        if date_filter.value:
            query += " AND ra.data = :date_filter"
            params["date_filter"] = date_filter.value
        if tipo_filter.value != "Todos":
            query += " AND ra.tipo = :tipo_filter"
            params["tipo_filter"] = tipo_filter.value

        query += " GROUP BY ra.id_registro_alimentacao ORDER BY ra.data DESC, ra.hora DESC"

        try:
            df = db.fetch_dataframe(query, params)
            data_cache["df"] = df
            if not df.empty:
                df_display = df.copy()
                df_display = format_date_column(df_display, 'data')
                df_display['hora'] = pd.to_datetime(df_display['hora'].astype(str)).dt.strftime('%H:%M')
                
                table_html = "<div style='overflow-x: auto;'><table class='custom-table'><thead><tr><th>ID</th><th>Data</th><th>Hora</th><th>Tipo</th><th>Descrição</th><th>Calorias</th></tr></thead><tbody>"
                for i, row in df_display.iterrows():
                    desc = safe_get_value(row, 'descricao', '')
                    desc_display = (desc[:42] + '...') if len(desc) > 45 else desc
                    row_color = '#f8f9fa' if i % 2 == 0 else 'white'
                    table_html += f"<tr style='background-color: {row_color};'><td>{safe_get_value(row, 'id_registro_alimentacao')}</td><td>{safe_get_value(row, 'data')}</td><td>{safe_get_value(row, 'hora')}</td><td>{safe_get_value(row, 'tipo')}</td><td>{desc_display}</td><td>{safe_get_value(row, 'calorias')}</td></tr>"
                table_html += "</tbody></table></div>"
                table_pane.object = table_html
            else:
                table_pane.object = "<div class='no-records'><h3>📭 Nenhum registro encontrado</h3><p>Adicione sua primeira refeição para começar!</p></div>"
        except Exception as e:
            table_pane.object = f"<div class='error-box'><strong>❌ Erro ao carregar dados:</strong> {e}</div>"

    def add_alimentacao(event):
        try:
            calorias = calorias_input.value
            if calorias is not None and calorias < 0:
                message_pane.object = "<div class='warning-box'>⚠️ Calorias devem ser um número positivo.</div>"
                return
            
            hora_val = time.fromisoformat(hora_input.value)
            descricoes = [line.strip() for line in descricao_input.value.split('\n') if line.strip()]
            if not descricoes:
                message_pane.object = "<div class='warning-box'>⚠️ A descrição é obrigatória.</div>"
                return

            query_reg = "INSERT INTO registro_alimentacao (id_usuario, data, hora, tipo, calorias) VALUES (:uid, :data, :hora, :tipo, :cal)"
            params_reg = {"uid": current_user["id"], "data": date_input.value, "hora": hora_val, "tipo": tipo_input.value, "cal": calorias}
            db.execute_query(query_reg, params_reg)

            query_id = """
            SELECT id_registro_alimentacao FROM registro_alimentacao
            WHERE id_usuario = :user_id
            ORDER BY id_registro_alimentacao DESC
            LIMIT 1
            """
            params = {
                "user_id": current_user["id"],
            }
            result_df = db.fetch_dataframe(query_id, params)
            print(result_df)
            new_id = int(result_df.iloc[0]['id_registro_alimentacao'])

            query_desc = "INSERT INTO registro_alimentacao_descricao (id_registro_alimentacao, descricao) VALUES (:id, :desc)"
            for desc in descricoes:
                db.execute_query(query_desc, {"id": new_id, "desc": desc})

            message_pane.object = "<div class='success-box'>✅ Registro adicionado com sucesso!</div>"
            clear_form()
            load_alimentacao_data()
        except ValueError:
            message_pane.object = "<div class='error-box'>❌ Formato de hora inválido. Use HH:MM.</div>"
        except Exception as e:
            message_pane.object = f"<div class='error-box'>❌ Erro ao adicionar registro: {e}</div>"

    def search_record(event):
        record_id = search_id_input.value
        if not record_id:
            search_message_pane.object = "<div class='warning-box'>⚠️ Por favor, digite um ID para buscar.</div>"
            return
        
        try:
            query = """
            SELECT ra.*, STRING_AGG(rad.descricao, '\n') AS descricao_agg
            FROM registro_alimentacao ra
            LEFT JOIN registro_alimentacao_descricao rad ON ra.id_registro_alimentacao = rad.id_registro_alimentacao
            WHERE ra.id_usuario = :uid AND ra.id_registro_alimentacao = :rid
            GROUP BY ra.id_registro_alimentacao
            """
            df = db.fetch_dataframe(query, {"uid": current_user["id"], "rid": record_id})

            if not df.empty:
                record = df.iloc[0]
                data_cache["current_record"] = record
                edit_date_input.value = record['data']
                edit_hora_input.value = record['hora'].strftime('%H:%M')
                edit_tipo_input.value = record['tipo']
                edit_calorias_input.value = record['calorias']
                edit_descricao_input.value = record['descricao_agg'] or ""
                
                for w in [edit_date_input, edit_hora_input, edit_tipo_input, edit_calorias_input, edit_descricao_input, edit_button, delete_button]:
                    w.disabled = False
                search_message_pane.object = f"<div class='success-box'>✅ Registro ID {record_id} encontrado!</div>"
            else:
                clear_edit_form()
                search_message_pane.object = "<div class='error-box'>❌ Registro não encontrado.</div>"
        except Exception as e:
            search_message_pane.object = f"<div class='error-box'>❌ Erro na busca: {e}</div>"

    def update_record(event):
        record_id = search_id_input.value
        if not record_id or data_cache["current_record"] is None:
            search_message_pane.object = "<div class='warning-box'>⚠️ Nenhum registro selecionado para edição.</div>"
            return
        
        try:
            calorias = edit_calorias_input.value
            if calorias is not None and calorias < 0:
                search_message_pane.object = "<div class='warning-box'>⚠️ Calorias devem ser um número positivo.</div>"
                return
            
            hora_val = time.fromisoformat(edit_hora_input.value)
            descricoes = [line.strip() for line in edit_descricao_input.value.split('\n') if line.strip()]
            if not descricoes:
                search_message_pane.object = "<div class='warning-box'>⚠️ A descrição é obrigatória.</div>"
                return

            query_upd = "UPDATE registro_alimentacao SET data=:data, hora=:hora, tipo=:tipo, calorias=:cal WHERE id_registro_alimentacao=:rid AND id_usuario=:uid"
            params_upd = {"data": edit_date_input.value, "hora": hora_val, "tipo": edit_tipo_input.value, "cal": int(calorias), "rid": record_id, "uid": current_user["id"]}
            db.execute_query(query_upd, params_upd)

            db.execute_query("DELETE FROM registro_alimentacao_descricao WHERE id_registro_alimentacao=:rid", {"rid": record_id})
            query_desc = "INSERT INTO registro_alimentacao_descricao (id_registro_alimentacao, descricao) VALUES (:rid, :desc)"
            for desc in descricoes:
                db.execute_query(query_desc, {"rid": record_id, "desc": desc})

            search_message_pane.object = "<div class='success-box'>✅ Registro atualizado com sucesso!</div>"
            load_alimentacao_data()
            clear_search_form()
        except Exception as e:
            search_message_pane.object = f"<div class='error-box'>❌ Erro ao atualizar: {e}</div>"

    def delete_record(event):
        record_id = search_id_input.value
        if not record_id or data_cache["current_record"] is None:
            search_message_pane.object = "<div class='warning-box'>⚠️ Nenhum registro selecionado para exclusão.</div>"
            return
        
        try:
            query = "DELETE FROM registro_alimentacao WHERE id_registro_alimentacao = :rid AND id_usuario = :uid"
            db.execute_query(query, {"rid": record_id, "uid": current_user["id"]})
            search_message_pane.object = "<div class='success-box'>✅ Registro excluído com sucesso!</div>"
            load_alimentacao_data()
            clear_search_form()
        except Exception as e:
            search_message_pane.object = f"<div class='error-box'>❌ Erro ao excluir: {e}</div>"

    def clear_form():
        date_input.value = date.today()
        hora_input.value = datetime.now().strftime("%H:%M")
        tipo_input.value = tipos_refeicao[0]
        calorias_input.value = 0
        descricao_input.value = ""
        message_pane.object = "<div class='info-box'>📝 Formulário pronto para novo registro.</div>"

    def clear_edit_form():
        for w in [edit_date_input, edit_hora_input, edit_tipo_input, edit_calorias_input, edit_descricao_input, edit_button, delete_button]:
            w.disabled = True
        
        edit_date_input.value = None
        edit_hora_input.value = ""
        edit_tipo_input.value = None
        edit_calorias_input.value = 0
        edit_descricao_input.value = ""
        
        data_cache["current_record"] = None

    def clear_search_form():
        search_id_input.value = None
        clear_edit_form()
        search_message_pane.object = "<div class='info-box'>🔍 Formulário pronto para nova busca.</div>"

    def back_to_main(event):
        navigate_to_main_page()

    add_button.on_click(add_alimentacao)
    back_button.on_click(back_to_main)
    clear_button.on_click(lambda e: clear_form())
    search_button.on_click(search_record)
    edit_button.on_click(update_record)
    delete_button.on_click(delete_record)
    clear_search_button.on_click(lambda e: clear_search_form())
    date_filter.param.watch(lambda e: load_alimentacao_data(), 'value')
    tipo_filter.param.watch(lambda e: load_alimentacao_data(), 'value')

    load_alimentacao_data()

    header = pn.pane.HTML("<h1>🍎 Gerenciamento de Alimentação</h1>")
    
    filters_section = pn.Column(pn.pane.HTML("<h2 class='section-header'>🔍 Filtros</h2>"), pn.Row(date_filter, tipo_filter), css_classes=['section-card'])
    records_section = pn.Column(pn.pane.HTML("<h2 class='section-header'>📋 Registros</h2>"), table_pane, css_classes=['section-card'])

    cadastro_tab = pn.Column(
        pn.Row(date_input, hora_input),
        pn.Row(tipo_input, calorias_input),
        descricao_input,
        pn.Row(add_button, clear_button, align='center'),
        message_pane
    )
    
    edit_tab = pn.Column(
        pn.Row(search_id_input, search_button, align='end'),
        pn.pane.HTML("<hr>"),
        pn.Row(edit_date_input, edit_hora_input),
        pn.Row(edit_tipo_input, edit_calorias_input),
        edit_descricao_input,
        pn.Row(edit_button, delete_button, clear_search_button, align='center'),
        search_message_pane
    )
    
    form_section = pn.Column(pn.pane.HTML("<h2 class='section-header'>📝 Formulário de Registro</h2>"), pn.Tabs(("📝 Cadastro", cadastro_tab), ("✏️ Editar/Excluir", edit_tab)), css_classes=['section-card'])

    main_content = pn.Column(header, filters_section, records_section, form_section, css_classes=['humor-container'], sizing_mode='stretch_width')
    
    return pn.Column(pn.Row(pn.Spacer(), back_button, margin=(10, 20, 0, 0)), main_content, sizing_mode='stretch_width', min_height=700)