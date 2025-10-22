from flask import Blueprint, render_template, request
from database.Local_dao import LocalDAO

bp_local = Blueprint('locais', __name__, url_prefix='/adm/locais')

"""
@bp_empregados.route('/incluir')  # /adm/empregados/incluir
def incluir():
    return render_template('adm/empregados/incluir.html', msg="", css_msg="")
"""

@bp_local.route('/consultar')  # /adm/empregados/consultar
def consultar():
    return render_template('adm/locais/consultar.html', locais=[], filtro_usado='')

@bp_local.route('/roda_consultar', methods=['POST'])  # /adm/empregados/roda_consultar
def roda_consultar():
    nme_local = request.form['nme_local']
    filtros = []

    if nme_local:
        filtros.append(('nme_local', 'ilike', f'%{nme_local}%'))

    filtro_usado = f'Nome do local: {nme_local or "Não informado"}'

    dao = LocalDAO()
    locais = dao.read_by_like('nme_local', nme_local)

    return render_template('adm/locais/consultar.html', locais=locais, filtro_usado=filtro_usado)


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