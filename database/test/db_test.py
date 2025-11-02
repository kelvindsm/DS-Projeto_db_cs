from database.db import Database
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

try:
    db = Database()
    print(f"Engine criado: {db.get_engine()}")

    # Teste de conexão e versão do PostgreSQL (copie do exemplo anterior)
    with db.get_engine().connect() as connection:
        result = connection.execute(text("SELECT version();"))
        pg_version = result.scalar_one()
        print(f"Conectado ao PostgreSQL - Versão: {pg_version}")

    print("\n--- Classes Mapeadas pelo Automap ---")
    if hasattr(db.DB, 'classes'):
        # Iterar diretamente sobre db.DB.classes (não precisa de _decl_class_registry.keys())
        for class_name_obj in db.DB.classes:  # O db.DB.classes é um iterable de classes mapeadas
            print(f" - {class_name_obj.__name__}")  # Pegue o nome da classe
    else:
        print("Automap ainda não preparou as classes.")
    print("------------------------------------\n")


except SQLAlchemyError as sa_err:
    print(f"Erro de SQLAlchemy durante a inicialização/conexão: {sa_err}")
    print("Verifique a URL da conexão, credenciais, host, porta e a existência do banco/esquema.")
except Exception as e:
    print(f"Um erro inesperado ocorreu: {e}")
