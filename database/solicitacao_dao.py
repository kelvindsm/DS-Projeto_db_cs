# Classe DAO para Solicitações (Serviços)
from database.model_dao import DAO

class SolicitacaoDAO(DAO):
    def __init__(self):
        super().__init__("tb_servico", "idt_servico")

    def get_solicitacoes_ativas(self):
        """
        Retorna todas as solicitações (serviços) ativas
        Joins com tabela de setores para obter nome do setor
        """
        try:
            sql = """
            SELECT 
                ts.idt_servico,
                ts.nme_servico,
                ts.num_dias_servico,
                ts.vlr_servico,
                ts.txt_modelo_servico,
                ts.sts_servico,
                ts.cod_setor,
                setor.nme_setor,
                setor.sgl_setor
            FROM cs.tb_servico as ts
            LEFT JOIN cs.tt_setor as setor ON ts.cod_setor = setor.idt_setor
            WHERE ts.sts_servico = 'A'
            ORDER BY ts.nme_servico ASC
            """
            
            result = self.execute_sql_and_fetch(sql)
            
            if result is None:
                return []
            
            solicitacoes = []
            for row in result:
                solicitacoes.append({
                    'idt_servico': row[0],
                    'nme_servico': row[1],
                    'num_dias_servico': row[2],
                    'vlr_servico': float(row[3]) if row[3] else 0,
                    'txt_modelo_servico': row[4],
                    'sts_servico': row[5],
                    'cod_setor': row[6],
                    'nme_setor': row[7],
                    'sgl_setor': row[8]
                })
            
            return solicitacoes
        except Exception as e:
            print(f"Erro ao obter solicitações ativas: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_solicitacoes_por_setor(self, cod_setor):
        """
        Retorna solicitações ativas de um setor específico
        """
        try:
            sql = """
            SELECT 
                ts.idt_servico,
                ts.nme_servico,
                ts.num_dias_servico,
                ts.vlr_servico,
                ts.txt_modelo_servico,
                ts.sts_servico,
                ts.cod_setor,
                setor.nme_setor,
                setor.sgl_setor
            FROM cs.tb_servico as ts
            LEFT JOIN cs.tt_setor as setor ON ts.cod_setor = setor.idt_setor
            WHERE ts.sts_servico = 'A' AND ts.cod_setor = :cod_setor
            ORDER BY ts.nme_servico ASC
            """
            
            result = self.execute_sql_and_fetch(sql, {'cod_setor': cod_setor})
            
            if result is None:
                return []
            
            solicitacoes = []
            for row in result:
                solicitacoes.append({
                    'idt_servico': row[0],
                    'nme_servico': row[1],
                    'num_dias_servico': row[2],
                    'vlr_servico': float(row[3]) if row[3] else 0,
                    'txt_modelo_servico': row[4],
                    'sts_servico': row[5],
                    'cod_setor': row[6],
                    'nme_setor': row[7],
                    'sgl_setor': row[8]
                })
            
            return solicitacoes
        except Exception as e:
            print(f"Erro ao obter solicitações por setor: {e}")
            import traceback
            traceback.print_exc()
            return []
