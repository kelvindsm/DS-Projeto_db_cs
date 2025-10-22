from flask import Blueprint, render_template, request

from database.tipo_ocorrencia_dao import TipoOcorrenciaDAO

bp_tpOcorrencias = Blueprint('ocorrencias', __name__, url_prefix='/adm/ocorrencias')

"""
@bp_emp.route('/incluir')  # /adm/ocorrencias/incluir
def incluir():
    return render_template('adm/ocorrencias/incluir.html', msg="", css_msg="")
"""

@bp_tpOcorrencias.route('/consultar')  # /adm/setor/consultar
def consultar():
    return render_template('adm/ocorrencias/consultar.html', tpOcorrencias=[], filtro_usado='')


@bp_tpOcorrencias.route('/roda_consultar', methods=['POST'])  # /adm/setor/roda_consultar
def roda_consultar():
    nme_tipo_ocorrencia = request.form['nme_tipo_ocorrencia']

    dao = TipoOcorrenciaDAO()

    if nme_tipo_ocorrencia:
        tpOcorrencias = dao.read_by_like('nme_tipo_ocorrencia', nme_tipo_ocorrencia)
    else:
        tpOcorrencias = dao.read_by_filters([('sts_tipo_ocorrencia', '=', 'A')])

    if tpOcorrencias is None:
        tpOcorrencias = []

    filtro_usado = f'Nome do tipo da ocorrencia: {nme_tipo_ocorrencia} or "Todos"'

    return render_template('adm/ocorrencias/consultar.html', tpOcorrencias=tpOcorrencias, filtro_usado=filtro_usado)


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