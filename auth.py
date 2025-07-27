import hashlib
from database import db

current_user = {"id": None, "nome": None}

def update_local_name(name):
    current_user["nome"] = name

def logout_user():
    current_user["id"] = None
    current_user["nome"] = None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    query = "SELECT id_usuario, nome FROM usuario WHERE email = :email AND senha = :senha"
    hashed_password = hash_password(password)
    result = db.execute_query(query, {"email": email, "senha": hashed_password})

    if result:
        user_data = result[0]
        current_user["id"] = user_data[0]
        current_user["nome"] = user_data[1]
        return True
    return False
