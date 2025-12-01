from flask import Blueprint, render_template, jsonify
from database.servico_dao import ServicoDAO
from database.setor_dao import SetorDAO
from database.solicitacao_dao import SolicitacaoDAO

bp_solicitante = Blueprint('solicitante', __name__, url_prefix='/solicitante')


@bp_solicitante.route('/solicitacoes_ativas')
def solicitacoes_ativas():
    """Exibe a página de solicitações ativas de serviços"""
    dao = SolicitacaoDAO()
    solicitacoes = dao.get_solicitacoes_ativas()
    
    # Obter lista de setores para filtro
    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
    
    return render_template('solicitante/solicitacoes_ativas.html', 
                         solicitacoes=solicitacoes, 
                         setores=setores,
                         filtro_usado='')


@bp_solicitante.route('/solicitacoes_ativas/filtrar', methods=['POST'])
def solicitacoes_ativas_filtrar():
    """Filtra solicitações ativas por setor"""
    from flask import request
    
    cod_setor = request.form.get('cod_setor', '')
    
    dao = SolicitacaoDAO()
    dao_setor = SetorDAO()
    
    if cod_setor:
        solicitacoes = dao.get_solicitacoes_por_setor(int(cod_setor))
        setor_selecionado = dao_setor.read_by_idt(int(cod_setor))
        filtro_usado = f'Setor: {setor_selecionado.nme_setor}' if setor_selecionado else 'Setor inválido'
    else:
        solicitacoes = dao.get_solicitacoes_ativas()
        filtro_usado = 'Todos os setores'
    
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
    
    return render_template('solicitante/solicitacoes_ativas.html',
                         solicitacoes=solicitacoes,
                         setores=setores,
                         filtro_usado=filtro_usado)


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
