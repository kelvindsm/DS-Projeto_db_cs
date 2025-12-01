from flask import Blueprint, render_template, jsonify
from database.servico_dao import ServicoDAO
from database.setor_dao import SetorDAO

bp_solicitante = Blueprint('solicitante', __name__, url_prefix='/solicitante')


@bp_solicitante.route('/graficos')
def graficos():
    return render_template('solicitante/graficos.html')


@bp_solicitante.route('/api/analise-valores-servicos')
def api_analise_valores_servicos():
    dao = ServicoDAO()
    dados = dao.get_analise_valores_por_setor()
    
    # Verifica se dados é None, vazio ou não é uma lista
    if not dados or not isinstance(dados, list) or len(dados) == 0:
        return jsonify({
            'setores': [],
            'minimos': [],
            'maximos': [],
            'medias': []
        })
    
    try:
        setores = [d['nme_setor'] for d in dados]
        minimos = [float(d['min_valor']) if d['min_valor'] is not None else 0 for d in dados]
        maximos = [float(d['max_valor']) if d['max_valor'] is not None else 0 for d in dados]
        medias = [float(d['media_valor']) if d['media_valor'] is not None else 0 for d in dados]
        
        return jsonify({
            'setores': setores,
            'minimos': minimos,
            'maximos': maximos,
            'medias': medias
        })
    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'setores': [],
            'minimos': [],
            'maximos': [],
            'medias': []
        })
