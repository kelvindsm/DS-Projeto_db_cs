from flask import Blueprint, render_template, request

from database.Empregado_dao import EmpregadoDAO
from database.Local_dao import LocalDAO

bp_empregados = Blueprint('empregados', __name__, url_prefix='/adm/empregados')

"""
@bp_empregados.route('/incluir')  # /adm/empregados/incluir
def incluir():
    return render_template('adm/empregados/incluir.html', msg="", css_msg="")
"""

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


"""
@bp_emp.route('/salvar_incluir', methods=['POST'])  # /adm/setor/salvar_incluir
def salvar_incluir():
    dao = SetorDAO()
    setor = dao.new_object()
    setor.sgl_setor = request.form['sgl_setor']
    setor.nme_setor = request.form['nme_setor']
    setor.eml_setor = request.form['eml_setor']
    setor.sts_setor = request.form['sts_setor']
    if dao.insert(setor):
        msg = f"Setor número {setor.idt_setor} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir setor!"
        css_msg = "erro"

    return render_template('adm/setor/incluir.html', msg=msg, css_msg=css_msg)
"""