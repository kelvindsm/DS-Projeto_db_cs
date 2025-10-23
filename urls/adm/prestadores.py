from flask import Blueprint, render_template, request
from database.Prestador_dao import PrestadorDAO
from database.setor_dao import SetorDAO


bp_prestadores = Blueprint('prestadores', __name__, url_prefix='/adm/prestadores')

@bp_prestadores.route('/incluir')
def incluir():
    dao = SetorDAO()
    lst_setores = dao.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/prestadores/incluir.html', msg="", css_msg="", lst_setores=lst_setores)

@bp_prestadores.route('/salvar_incluir', methods=['POST'])  # /adm/prestadores/incluir
def salvar_incluir():
    dao = PrestadorDAO()
    prestadores = dao.new_object()
    prestadores.nme_prestador = request.form['nme_prestador']
    prestadores.eml_prestador = request.form['eml_prestador']
    prestadores.sts_prestador = request.form['sts_prestador']
    prestadores.cod_setor = request.form['cod_setor']

    if dao.insert(prestadores):
        msg = f"Serviço número {prestadores.idt_prestador} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir serviço!"
        css_msg = "erro"

    dao_setor = SetorDAO()
    lst_setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])

    return render_template('adm/prestadores/incluir.html', msg="", css_msg="", lst_setores=lst_setores)