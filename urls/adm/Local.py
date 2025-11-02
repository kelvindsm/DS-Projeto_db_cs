from flask import Blueprint, render_template, request
from database.Local_dao import LocalDAO
from database.setor_dao import SetorDAO

bp_locais = Blueprint('locais', __name__, url_prefix='/adm/locais')

# INSERT
@bp_locais.route('/incluir')  # /adm/locais/incluir
def incluir():
    dao = SetorDAO()
    lst_setores = dao.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/locais/incluir.html', msg="", css_msg="", lst_setores=lst_setores)


@bp_locais.route('/salvar_incluir', methods=['POST'])  # /adm/locais/incluir
def salvar_incluir():
    dao = LocalDAO()
    local = dao.new_object()
    local.nme_local = request.form['nme_local']
    local.lat_local = request.form['lat_local']
    local.lgt_local = request.form['lgt_local']
    local.sts_local = request.form['sts_local']
    local.cod_setor = request.form['cod_setor']

    if dao.insert(local):
        msg = f"Local número {local.idt_local} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir Local!"
        css_msg = "erro"

    dao_setor = SetorDAO()
    lst_setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])

    return render_template('adm/locais/incluir.html', msg=msg, css_msg=css_msg, lst_setores=lst_setores)

# SELECT

@bp_locais.route('/consultar')  # /adm/empregados/consultar
def consultar():
    return render_template('adm/locais/consultar.html', locais=[], filtro_usado='')

@bp_locais.route('/roda_consultar', methods=['POST'])  # /adm/empregados/roda_consultar
def roda_consultar():
    nme_local = request.form['nme_local']
    filtros = []

    if nme_local:
        filtros.append(('nme_local', 'ilike', f'%{nme_local}%'))

    filtro_usado = f'Nome do local: {nme_local or "Não informado"}'

    dao = LocalDAO()
    locais = dao.read_by_like('nme_local', nme_local)

    return render_template('adm/locais/consultar.html', locais=locais, filtro_usado=filtro_usado)

# UPDATE

@bp_locais.route('/atualizar')
def atualizar():
    return render_template('adm/locais/atualizar.html', locais=[], filtro_usado='', msg='', css_msg='')


@bp_locais.route('/roda_atualizar', methods=['POST'])
def roda_atualizar():
    nme_local = request.form['nme_local']
    filtro_usado = f'Descrição do Local: {nme_local}'
    dao = LocalDAO()
    locais = dao.read_by_like('nme_local', nme_local)
    return render_template('adm/locais/atualizar.html', locais=locais, filtro_usado=filtro_usado, msg='', css_msg='')


@bp_locais.route('/alterar/<int:idt>')
def alterar(idt):
    dao = LocalDAO()
    local = dao.read_by_idt(idt)
    if not local:
        msg = 'Local não encontrado para alteração.'
        css_msg = 'erro'
        return render_template('adm/locais/atualizar.html', msg=msg, css_msg=css_msg, locais=[], filtro_usado='')
    return render_template('adm/locais/alterar.html', local=local, msg='', css_msg='')


@bp_locais.route('/salvar_alterar', methods=['POST'])
def salvar_alterar():
    dao = LocalDAO()
    try:
        idt_local = int(request.form.get('idt_local'))
    except (TypeError, ValueError):
        idt_local = None

    local = dao.read_by_idt(idt_local) if idt_local is not None else None
    if not local:
        msg = 'Local não encontrado para alteração.'
        css_msg = 'erro'
        return render_template('adm/locais/atualizar.html', msg=msg, css_msg=css_msg, locais=[], filtro_usado='')

    local.dsc_local = request.form['dsc_local']
    local.sts_local = request.form['sts_local']

    if dao.update(local):
        msg = f"Local {local.idt_local} atualizado com sucesso!"
        css_msg = 'sucesso'
    else:
        msg = 'Erro ao tentar atualizar local!'
        css_msg = 'erro'

    return render_template('adm/locais/alterar.html', local=local, msg=msg, css_msg=css_msg)


@bp_locais.route('/excluir/<int:idt>')
def excluir(idt):
    dao = LocalDAO()
    if dao.delete(idt):
        msg = 'Local excluído com sucesso!'
        css_msg = "sucesso"
    else:
        msg = 'Falha ao tentar excluir local! Verifique se existe alguma pendência!'
        css_msg = "erro"
    local = dao.read_by_idt(idt)
    return render_template('adm/locais/atualizar.html', msg=msg, css_msg=css_msg, locais=[], filtro_usado='')