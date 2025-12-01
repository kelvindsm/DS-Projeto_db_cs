from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base


class Database:
    USER = 'postgres'
    PASSWORD = 'ceub123456'
    HOST = 'localhost'
    PORT = 5432
    DATABASE = 'db_cs'

    DB_URL = f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

    # Criar o mapeamento do banco de dados db_central_servico
    def __init__(self):
        self.engine = create_engine(self.DB_URL)
        self.DB = automap_base()
        self.DB.prepare(autoload_with=self.engine, schema="cs")
        self.session_factory = sessionmaker(bind=self.engine)
        self.ses = self.session_factory()

    def get_session(self):
        return self.ses

    def get_engine(self):
        return self.engine
