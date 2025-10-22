# Classe Genérica de "Model"


from sqlalchemy import and_, text
from sqlalchemy import func
from database.db import Database


class DAO:
    def __init__(self, table_name, idt_column_name):
        self.db = Database()
        self.ses = self.db.get_session()
        self.table = getattr(self.db.DB.classes, table_name)  # Obtém a classe da tabela dinamicamente
        self.idt_column_name = idt_column_name
        self.table_name = table_name

    def read_by_idt(self, idt):
        return self.ses.query(self.table).filter(getattr(self.table, self.idt_column_name) == idt).first()

    def read_by_field(self, field, value):
        try:
            obj = self.ses.query(self.table).filter(getattr(self.table, field) == value).first()
            return obj
        except Exception as e:
            print(f"Erro ao ler em {self.table_name} e {field}: {e}")
            return None

    def read_by_like(self, field, value):
        try:
            objs = self.ses.query(self.table).filter(
                getattr(self.table, field).like(f"%{value}%")).all()  # Retorna uma lista
            return objs
        except Exception as e:
            print(f"Erro ao ler em {self.table_name} e {field} com LIKE: {e}")
            return None

    def read_by_interval(self, field, start, end):
        try:
            objs = self.ses.query(self.table).filter(
                and_(
                    getattr(self.table, field) >= start,
                    getattr(self.table, field) <= end
                )
            ).all()
            return objs
        except Exception as e:
            print(f"Erro ao ler em {self.table_name} e {field} com intervalo: {e}")
            return None

    def read_by_filters(self, filters):
        try:
            conditions = []
            for field, operator, value in filters:
                operator = operator.lower()
                column = getattr(self.table, field)  # Obtém a coluna

                if operator == "=":
                    condition = column == value
                elif operator == "!=":
                    condition = column != value
                elif operator == ">":
                    condition = column > value
                elif operator == ">=":
                    condition = column >= value
                elif operator == "<":
                    condition = column < value
                elif operator == "<=":
                    condition = column <= value
                elif operator == "like":
                    condition = column.like(f"%{value}%")  # Use diretamente na coluna
                elif operator == "ilike":  # Para pesquisas case-insensitive
                    condition = column.ilike(f"%{value}%")
                else:
                    raise ValueError(f"Operador '{operator}' não suportado.")
                conditions.append(condition)

            objs = self.ses.query(self.table).filter(and_(*conditions)).all()
            return objs


        except Exception as e:
            print(f"Erro ao ler registros em {self.table_name} com filtro(s): {e}")
            return None

    def read_all(self):
        return self.ses.query(self.table).all()

    def count(self):
        try:
            num_count = self.ses.query(func.count()).select_from(self.table).scalar()
            return num_count
        except Exception as e:
            print(f"Erro ao contar registros em {self.table_name}: {e}")
            return None

    def count_filters(self, filters):
        try:
            conditions = []
            for field, operator, value in filters:
                operator = operator.lower()
                column = getattr(self.table, field)  # Obtém a coluna

                if operator == "=":
                    condition = getattr(self.table, field) == value
                elif operator == "!=":
                    condition = getattr(self.table, field) != value
                elif operator == ">":
                    condition = getattr(self.table, field) > value
                elif operator == ">=":
                    condition = getattr(self.table, field) >= value
                elif operator == "<":
                    condition = getattr(self.table, field) < value
                elif operator == "<=":
                    condition = getattr(self.table, field) <= value
                elif operator == "like":
                    condition = column.like(f"%{value}%")  # Use diretamente na coluna
                elif operator == "ilike":  # Para pesquisas case-insensitive
                    condition = column.ilike(f"%{value}%")
                else:
                    raise ValueError(f"Operador '{operator}' não suportado.")
                conditions.append(condition)

            num_count = self.ses.query(func.count()).select_from(self.table).filter(
                and_(*conditions)).scalar()  # Usando AND para multiplos filtros
            return num_count


        except Exception as e:
            print(f"Erro ao contar registros em {self.table_name} com filtro(s): {e}")
            return None

    def execute_sql_and_fetch(self, sql_string, params=None):
        try:
            if params:
                result = self.ses.execute(text(sql_string), params)
            else:
                result = self.ses.execute(text(sql_string))
            return result.fetchall()
        except Exception as e:
            print(f"Erro ao executar SQL: {e}")
            return None

    def new_object(self):
        return self.table()

    def insert(self, obj):
        self.ses.add(obj)
        try:
            self.ses.commit()
            return obj
        except Exception as e:
            self.ses.rollback()
            print(f"Erro ao inserir em {self.table_name}: {e}")
            return None

    def update(self, obj):
        with self.db.get_session() as ses:
            # Se o obj já veio da sessão, apenas commit
            # Se o obj é um "detached" object, use merge
            try:
                if not ses.query(obj.__class__).filter(
                        getattr(obj, self.idt_column_name) == getattr(obj, self.idt_column_name)).first():
                    # Se não foi encontrado na sessão atual, tente "merge"
                    obj = ses.merge(obj)
                ses.commit()
                ses.refresh(obj)  # Opcional: recarregar o objeto após o commit
                return obj
            except Exception as e:
                ses.rollback()
                print(f"Erro ao atualizar em {self.table_name}: {e}")
                return None

    def delete(self, idt):
        obj = self.read_by_idt(idt)
        if obj:
            try:
                self.ses.delete(obj)
                self.ses.commit()
                return True
            except Exception as e:
                self.ses.rollback()
                print(f"Erro ao deletar em {self.table_name}: {e}")
                return False
        return False
