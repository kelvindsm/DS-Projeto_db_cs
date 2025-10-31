from flask import Blueprint, render_template, request

from database.Prestador_dao import PrestadorDAO

bp_prestadores = Blueprint('prestadores', __name__, url_prefix='/adm/prestadores')


@bp_prestadores.route('/atualizar')
def atualizar():
    return render_template('adm/prestadores/atualizar.html', prestadores=[], filtro_usado='', msg='', css_msg='')


@bp_prestadores.route('/roda_atualizar', methods=['POST'])
def roda_atualizar():
    nme_prestador = request.form['nme_prestador']
    filtro_usado = f'Nome do Prestador: {nme_prestador}'
    dao = PrestadorDAO()
    prestadores = dao.read_by_like('nme_prestador', nme_prestador)
    if prestadores is None:
        prestadores = []
    return render_template('adm/prestadores/atualizar.html', prestadores=prestadores, filtro_usado=filtro_usado, msg='', css_msg='')


@bp_prestadores.route('/alterar/<int:idt>')
def alterar(idt):
    dao = PrestadorDAO()
    prestador = dao.read_by_idt(idt)
    if not prestador:
        msg = 'Prestador não encontrado para alteração.'
        css_msg = 'erro'
        return render_template('adm/prestadores/atualizar.html', msg=msg, css_msg=css_msg, prestadores=[], filtro_usado='')
    return render_template('adm/prestadores/alterar.html', prestador=prestador, msg='', css_msg='')


@bp_prestadores.route('/salvar_alterar', methods=['POST'])
def salvar_alterar():
    dao = PrestadorDAO()
    try:
        idt_prestador = int(request.form.get('idt_prestador'))
    except (TypeError, ValueError):
        idt_prestador = None

    prestador = dao.read_by_idt(idt_prestador) if idt_prestador is not None else None
    if not prestador:
        msg = 'Prestador não encontrado para alteração.'
        css_msg = 'erro'
        return render_template('adm/prestadores/atualizar.html', msg=msg, css_msg=css_msg, prestadores=[], filtro_usado='')

    prestador.nme_prestador = request.form['nme_prestador']
    prestador.eml_prestador = request.form['eml_prestador']
    prestador.sts_prestador = request.form['sts_prestador']

    if dao.update(prestador):
        msg = f"Prestador {prestador.idt_prestador} atualizado com sucesso!"
        css_msg = 'sucesso'
    else:
        msg = 'Erro ao tentar atualizar prestador!'
        css_msg = 'erro'

    return render_template('adm/prestadores/alterar.html', prestador=prestador, msg=msg, css_msg=css_msg)

@bp_prestadores.route('/excluir/<int:idt>')
def excluir(idt):
    dao = PrestadorDAO()
    if dao.delete(idt):
        msg = 'Prestador excluído com sucesso!'
        css_msg = "sucesso"
    else:
        msg = 'Falha ao tentar excluir prestador! Verifique se existe alguma pendência!'
        css_msg = "erro"
    prestador = dao.read_by_idt(idt)
    return render_template('adm/prestadores/atualizar.html', msg=msg, css_msg=css_msg, prestadores=[], filtro_usado='')

