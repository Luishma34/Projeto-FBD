import pandas as pd

def format_date_column(df, column_name, date_format='%d/%m/%Y'):
    """
    Formata uma coluna de data no DataFrame de forma segura

    Args:
        df: DataFrame do pandas
        column_name: Nome da coluna a ser formatada
        date_format: Formato de saída da data

    Returns:
        DataFrame com coluna formatada
    """
    if df.empty or column_name not in df.columns:
        return df

    try:
        # Verificar se já é datetime
        if not pd.api.types.is_datetime64_any_dtype(df[column_name]):
            # Tentar converter para datetime
            df[column_name] = pd.to_datetime(df[column_name], errors='coerce')

        # Formatar para string
        df[column_name] = df[column_name].dt.strftime(date_format)

        # Substituir valores NaT por string vazia
        df[column_name] = df[column_name].fillna('')

    except Exception as e:
        print(f"Erro ao formatar coluna {column_name}: {e}")
        # Em caso de erro, converter diretamente para string
        df[column_name] = df[column_name].astype(str)

    return df

def safe_get_value(row, column_name, default=''):
    """
    Obtém valor de uma coluna de forma segura, tratando valores nulos

    Args:
        row: Linha do DataFrame
        column_name: Nome da coluna
        default: Valor padrão se for nulo

    Returns:
        Valor da coluna ou valor padrão
    """
    try:
        value = row[column_name]
        if pd.isna(value) or value is None:
            return default
        return str(value)
    except (KeyError, IndexError):
        return default