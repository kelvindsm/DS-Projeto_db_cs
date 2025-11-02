from flask import Blueprint, render_template, request
from database.Empregado_dao import EmpregadoDAO
from database.Local_dao import LocalDAO

bp_empregados = Blueprint('empregados', __name__, url_prefix='/adm/empregados')

@bp_empregados.route('/incluir')  # /adm/empregados/incluir
def incluir():
    dao = LocalDAO()
    lst_local = dao.read_by_filters([('sts_local', '=', 'A')])
    return render_template('adm/empregados/incluir.html', msg="", css_msg="", lst_local=lst_local)

@bp_empregados.route('/salvar_incluir', methods=['POST'])  # /adm/setor/salvar_incluir
def salvar_incluir():
    dao = EmpregadoDAO()
    empregado = dao.new_object()
    empregado.nme_empregado = request.form['nme_empregado']
    empregado.eml_empregado = request.form['eml_empregado']
    empregado.sts_empregado = request.form['sts_empregado']
    empregado.mat_empregado = request.form['mat_empregado']

    empregado.tel_empregado = request.form['tel_empregado']
    empregado.rml_empregado = request.form['rml_empregado']
    empregado.pwd_empregado = request.form['pwd_empregado']
    empregado.cod_local = request.form['cod_local']
    #inserir locais
    if dao.insert(empregado):
        msg = f"Empregado número {empregado.idt_empregado} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir empregado!"
        css_msg = "erro"

    dao_local = LocalDAO()
    lst_local = dao_local.read_by_filters([('sts_local', '=', 'A')])

    return render_template('adm/empregados/incluir.html', msg=msg, css_msg=css_msg, lst_local=lst_local,)