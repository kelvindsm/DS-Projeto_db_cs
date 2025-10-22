# Classe DAO para a entidade "tb_setor"
from database.model_dao import DAO


class EmpregadoDAO(DAO):
    def __init__(self):
        super().__init__("tb_empregado", "idt_empregado")
