from flask import Blueprint, render_template, request

from database.Prestador_dao import PrestadorDAO
from database.setor_dao import SetorDAO

bp_prestadores = Blueprint('prestadores', __name__, url_prefix='/adm/prestadores')

"""
@bp_emp.route('/incluir')  # /adm/prestadores/incluir
def incluir():
    return render_template('adm/prestadores/incluir.html', msg="", css_msg="")
"""

@bp_prestadores.route('/consultar')  # /adm/prestadores/consultar
def consultar():
    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/prestadores/consultar.html', prestadores=[], setores=setores, filtro_usado='')

@bp_prestadores.route('/roda_consultar', methods=['POST'])  # /adm/empregados/roda_consultar
def roda_consultar():
    nme_prestador = request.form['nme_prestador']
    cod_setor = request.form['cod_setor']
    filtros = []

    if nme_prestador:
        filtros.append(('nme_prestador', 'ilike', f'%{nme_prestador}%'))
    if cod_setor:
        filtros.append(('cod_setor', '=', int(cod_setor)))
    filtro_usado = f'Nome do Empregado: {nme_prestador or "Não informado"} / Código do Setor: {cod_setor or "Todos"}'

    # filtro_usado = f'Nome do empregado: {nme_empregado}'
    dao = PrestadorDAO()
    prestadores = dao.read_by_like('nme_prestador', nme_prestador)

    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])

    return render_template('adm/prestadores/consultar.html', prestadores=prestadores, setores=setores, filtro_usado=filtro_usado)


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