import pandas as pd

def format_date_column(df, column_name, date_format='%d/%m/%Y'):
    if df.empty or column_name not in df.columns:
        return df

    try:
        if not pd.api.types.is_datetime64_any_dtype(df[column_name]):

            df[column_name] = pd.to_datetime(df[column_name], errors='coerce')

        df[column_name] = df[column_name].dt.strftime(date_format)

        df[column_name] = df[column_name].fillna('')

    except Exception as e:
        print(f"Erro ao formatar coluna {column_name}: {e}")
        df[column_name] = df[column_name].astype(str)

    return df

def safe_get_value(row, column_name, default=''):
    try:
        value = row[column_name]
        if pd.isna(value) or value is None:
            return default
        return str(value)
    except (KeyError, IndexError):
        return default