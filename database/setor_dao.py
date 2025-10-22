# Classe DAO para a entidade "tb_setor"
from database.model_dao import DAO


class SetorDAO(DAO):
    def __init__(self):
        super().__init__("tt_setor", "idt_setor")
