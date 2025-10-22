# Classe DAO para a entidade "tb_setor"
from database.model_dao import DAO

class TipoOcorrenciaDAO(DAO):
    def __init__(self):
        super().__init__("tt_tipo_ocorrencia", "idt_tipo_ocorrencia")
