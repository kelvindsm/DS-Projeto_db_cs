from flask import Blueprint, render_template, request

from database.tipo_ocorrencia_dao import TipoOcorrenciaDAO

bp_ocorrencias = Blueprint('ocorrencias', __name__, url_prefix='/adm/ocorrencias')


@bp_ocorrencias.route('/atualizar')
def atualizar():
    return render_template('adm/ocorrencias/atualizar.html', ocorrencias=[], filtro_usado='', msg='', css_msg='')


@bp_ocorrencias.route('/roda_atualizar', methods=['POST'])
def roda_atualizar():
    dsc_tipo_ocorrencia = request.form['dsc_tipo_ocorrencia']
    filtro_usado = f'Descrição da Ocorrência: {dsc_tipo_ocorrencia}'
    dao = TipoOcorrenciaDAO()
    ocorrencias = dao.read_by_like('dsc_tipo_ocorrencia', dsc_tipo_ocorrencia)
    if ocorrencias is None:
        ocorrencias = []
    return render_template('adm/ocorrencias/atualizar.html', ocorrencias=ocorrencias, filtro_usado=filtro_usado, msg='', css_msg='')


@bp_ocorrencias.route('/alterar/<int:idt>')
def alterar(idt):
    dao = TipoOcorrenciaDAO()
    ocorrencia = dao.read_by_idt(idt)
    if not ocorrencia:
        msg = 'Tipo de ocorrência não encontrado para alteração.'
        css_msg = 'erro'
        return render_template('adm/ocorrencias/atualizar.html', msg=msg, css_msg=css_msg, ocorrencias=[], filtro_usado='')
    return render_template('adm/ocorrencias/alterar.html', ocorrencia=ocorrencia, msg='', css_msg='')


@bp_ocorrencias.route('/salvar_alterar', methods=['POST'])
def salvar_alterar():
    dao = TipoOcorrenciaDAO()

    try:
        idt_tipo_ocorrencia = int(request.form.get('idt_tipo_ocorrencia'))
    except (TypeError, ValueError):
        idt_tipo_ocorrencia = None

    ocorrencia = dao.read_by_idt(idt_tipo_ocorrencia) if idt_tipo_ocorrencia is not None else None
    if not ocorrencia:
        msg = 'Tipo de ocorrência não encontrado para alteração.'
        css_msg = 'erro'
        return render_template('adm/ocorrencias/atualizar.html', msg=msg, css_msg=css_msg, ocorrencias=[], filtro_usado='')

    ocorrencia.dsc_tipo_ocorrencia = request.form['dsc_tipo_ocorrencia']
    ocorrencia.sts_tipo_ocorrencia = request.form['sts_tipo_ocorrencia']

    if dao.update(ocorrencia):
        msg = f"Tipo de ocorrência {ocorrencia.idt_tipo_ocorrencia} atualizado com sucesso!"
        css_msg = 'sucesso'
    else:
        msg = 'Erro ao tentar atualizar tipo de ocorrência!'
        css_msg = 'erro'

    return render_template('adm/ocorrencias/alterar.html', ocorrencia=ocorrencia, msg=msg, css_msg=css_msg)

@bp_ocorrencias.route('/excluir/<int:idt>')
def excluir(idt):
    dao = TipoOcorrenciaDAO()
    if dao.delete(idt):
        msg = 'Ocorrencia excluído com sucesso!'
        css_msg = "sucesso"
    else:
        msg = 'Falha ao tentar excluir ocorrência! Verifique se existe alguma pendência!'
        css_msg = "erro"
    ocorrencia = dao.read_by_idt(idt)
    return render_template('adm/ocorrencias/atualizar.html', msg=msg, css_msg=css_msg, ocorrencias=[], filtro_usado='')

