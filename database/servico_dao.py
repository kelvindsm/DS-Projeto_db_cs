# Classe DAO para a entidade "tb_setor"

from database.model_dao import DAO
from sqlalchemy import func, text

class ServicoDAO(DAO):
    def __init__(self):
        super().__init__("tb_servico", "idt_servico")

    def get_analise_valores_por_setor(self):
        try:
            sql = """
            SELECT 
                ts.nme_setor,
                MIN(CAST(ts_servico.vlr_servico AS NUMERIC)) as min_valor,
                MAX(CAST(ts_servico.vlr_servico AS NUMERIC)) as max_valor,
                AVG(CAST(ts_servico.vlr_servico AS NUMERIC)) as media_valor,
                COUNT(ts_servico.idt_servico) as total_servicos
            FROM cs.tb_servico as ts_servico
            INNER JOIN cs.tt_setor as ts ON ts_servico.cod_setor = ts.idt_setor
            GROUP BY ts.nme_setor, ts.idt_setor
            ORDER BY ts.nme_setor
            """
            
            result = self.execute_sql_and_fetch(sql)
            
            if result is None:
                return []
            
            dados = []
            for row in result:
                dados.append({
                    'nme_setor': row[0],
                    'min_valor': row[1],
                    'max_valor': row[2],
                    'media_valor': row[3],
                    'total_servicos': row[4]
                })
            
            return dados
        except Exception as e:
            print(f"Erro ao obter análise de valores por setor: {e}")
            import traceback
            traceback.print_exc()
            return []
