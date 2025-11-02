from flask import Blueprint, render_template, request

from database.Empregado_dao import EmpregadoDAO
from database.Local_dao import LocalDAO

bp_empregados = Blueprint('empregados', __name__, url_prefix='/adm/empregados')

# INSERT
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

@bp_empregados.route('/consultar')  # /adm/empregados/consultar
def consultar():
    dao_local = LocalDAO()
    locais = dao_local.read_by_filters([('sts_local', '=', 'A')])
    return render_template('adm/empregados/consultar.html', empregados=[], locais=locais, filtro_usado='')

@bp_empregados.route('/roda_consultar', methods=['POST'])  # /adm/empregados/roda_consultar
def roda_consultar():
    nme_empregado = request.form['nme_empregado']
    cod_local = request.form['cod_local']
    filtros = []

    if nme_empregado:
        filtros.append(('nme_empregado', 'ilike', f'%{nme_empregado}%'))
    if cod_local:
        filtros.append(('cod_local', '=', int(cod_local)))
    filtro_usado = f'Nome do Empregado: {nme_empregado or "Não informado"} / Código do Setor: {cod_local or "Todos"}'

    # filtro_usado = f'Nome do empregado: {nme_empregado}'
    dao = EmpregadoDAO()
    empregados = dao.read_by_like('nme_empregado', nme_empregado)

    dao_local = LocalDAO()
    locais = dao_local.read_by_filters([('sts_local', '=', 'A')])

    return render_template('adm/empregados/consultar.html', empregados=empregados, locais=locais, filtro_usado=filtro_usado)
