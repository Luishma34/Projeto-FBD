import hashlib
from database import db

# Variável global para usuário logado
current_user = {"id": None, "nome": None}

def logout_user():
    """Desloga o usuário atual, limpando os dados da sessão."""
    current_user["id"] = None
    current_user["nome"] = None

def hash_password(password):
    """Cria hash da senha"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    """Autentica usuário"""
    query = "SELECT id_usuario, nome FROM usuario WHERE email = :email AND senha = :senha"
    hashed_password = hash_password(password)
    result = db.execute_query(query, {"email": email, "senha": hashed_password})

    if result:
        user_data = result[0]
        current_user["id"] = user_data[0]
        current_user["nome"] = user_data[1]
        return True
    return False

def create_test_user():
    """Cria um usuário de teste"""
    try:
        # Verificar se usuário já existe
        check_query = "SELECT COUNT(*) FROM usuario WHERE email = 'test@test.com'"
        result = db.execute_query(check_query)
        
        if result[0][0] == 0:  # Usuário não existe
            insert_query = """
            INSERT INTO usuario (nome, email, senha, data_nascimento, sexo)
            VALUES ('Usuário Teste', 'test@test.com', :senha, '1990-01-01', 'Masculino')
            """
            hashed_password = hash_password("123456")
            db.execute_query(insert_query, {"senha": hashed_password})
            print("Usuário de teste criado: test@test.com / 123456")
    except Exception as e:
        print(f"Erro ao criar usuário de teste: {e}")