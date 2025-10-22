# Classe DAO para a entidade "tb_setor"
from database.model_dao import DAO

class ServicoDAO(DAO):
    def __init__(self):
        super().__init__("tb_servico", "idt_servico")
