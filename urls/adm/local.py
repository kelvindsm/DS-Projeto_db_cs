from flask import Blueprint, render_template, request

from database.Local_dao import LocalDAO

bp_locais = Blueprint('locais', __name__, url_prefix='/adm/locais')


@bp_locais.route('/atualizar')
def atualizar():
    return render_template('adm/locais/atualizar.html', locais=[], filtro_usado='', msg='', css_msg='')


@bp_locais.route('/roda_atualizar', methods=['POST'])
def roda_atualizar():
    dsc_local = request.form['dsc_local']
    filtro_usado = f'Descrição do Local: {dsc_local}'
    dao = LocalDAO()
    locais = dao.read_by_like('dsc_local', dsc_local)
    if locais is None:
        locais = []
    return render_template('adm/locais/atualizar.html', locais=locais, filtro_usado=filtro_usado, msg='', css_msg='')


@bp_locais.route('/alterar/<int:idt>')
def alterar(idt):
    dao = LocalDAO()
    local = dao.read_by_idt(idt)
    if not local:
        msg = 'Local não encontrado para alteração.'
        css_msg = 'erro'
        return render_template('adm/locais/atualizar.html', msg=msg, css_msg=css_msg, locais=[], filtro_usado='')
    return render_template('adm/locais/alterar.html', local=local, msg='', css_msg='')


@bp_locais.route('/salvar_alterar', methods=['POST'])
def salvar_alterar():
    dao = LocalDAO()
    try:
        idt_local = int(request.form.get('idt_local'))
    except (TypeError, ValueError):
        idt_local = None

    local = dao.read_by_idt(idt_local) if idt_local is not None else None
    if not local:
        msg = 'Local não encontrado para alteração.'
        css_msg = 'erro'
        return render_template('adm/locais/atualizar.html', msg=msg, css_msg=css_msg, locais=[], filtro_usado='')

    local.dsc_local = request.form['dsc_local']
    local.sts_local = request.form['sts_local']

    if dao.update(local):
        msg = f"Local {local.idt_local} atualizado com sucesso!"
        css_msg = 'sucesso'
    else:
        msg = 'Erro ao tentar atualizar local!'
        css_msg = 'erro'

    return render_template('adm/locais/alterar.html', local=local, msg=msg, css_msg=css_msg)


@bp_locais.route('/excluir/<int:idt>')
def excluir(idt):
    dao = LocalDAO()
    if dao.delete(idt):
        msg = 'Local excluído com sucesso!'
        css_msg = "sucesso"
    else:
        msg = 'Falha ao tentar excluir local! Verifique se existe alguma pendência!'
        css_msg = "erro"
    local = dao.read_by_idt(idt)
    return render_template('adm/locais/atualizar.html', msg=msg, css_msg=css_msg, locais=[], filtro_usado='')

