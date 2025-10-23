from flask import Blueprint, render_template, request
from database.Local_dao import LocalDAO
from database.setor_dao import SetorDAO


bp_locais = Blueprint('locais', __name__, url_prefix='/adm/locais')


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
        msg = f"Serviço número {local.idt_local} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir serviço!"
        css_msg = "erro"

    dao_setor = SetorDAO()
    lst_setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])

    return render_template('adm/locais/incluir.html', msg=msg, css_msg=css_msg, lst_setores=lst_setores)