import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
print(f"Conectando ao banco de dados {DB_NAME} no host {DB_HOST} com usuário {DB_USER}")
# Configuração do banco de dados
#DATABASE_URL = "postgresql://admin:admin@localhost:5432/projeto_fbd"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)

    def get_connection(self):
        return psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        # return psycopg2.connect(
        #     host="localhost",
        #     database="projeto_fbd",
        #     user="admin",
        #     password="admin",
        #     port="5432"
        # )
    
    def execute_query(self, query, params=None):
        """Executa uma query e retorna os resultados"""
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            if result.returns_rows:
                return result.fetchall()
            conn.commit()
            return None
    
    def fetch_dataframe(self, query, params=None):
        """Executa uma query e retorna um DataFrame"""
        with self.engine.connect() as conn:
            return pd.read_sql(text(query), conn, params=params or {})

db = DatabaseManager()