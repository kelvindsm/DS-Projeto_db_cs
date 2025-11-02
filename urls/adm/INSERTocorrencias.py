from flask import Blueprint, render_template, request
from database.tipo_ocorrencia_dao import TipoOcorrenciaDAO

bp_ocorrencias = Blueprint('ocorrencias', __name__, url_prefix='/adm/ocorrencias')

@bp_ocorrencias.route('/incluir')  # /adm/ocorrencias/incluir
def incluir():
    return render_template('adm/ocorrencias/incluir.html', msg="", css_msg="")


@bp_ocorrencias.route('/salvar_incluir', methods=['POST'])  # /adm/ocorrencias/salvar_incluir
def salvar_incluir():
    dao = TipoOcorrenciaDAO()
    ocorrencia = dao.new_object()
    ocorrencia.nme_tipo_ocorrencia = request.form['nme_tipo_ocorrencia']
    ocorrencia.tpo_tipo_ocorrencia = request.form['tpo_tipo_ocorrencia']
    ocorrencia.sts_tipo_ocorrencia = request.form['sts_tipo_ocorrencia']
    ocorrencia.txt_modelo_ocorrencia = request.form['txt_modelo_ocorrencia']

    if dao.insert(ocorrencia):
        msg = f"Ocorrência número {ocorrencia.idt_tipo_ocorrencia} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir ocorrencia!"
        css_msg = "erro"

    return render_template('adm/ocorrencias/incluir.html', msg=msg, css_msg=css_msg)
