from flask import Blueprint, render_template, request

from database.Empregado_dao import EmpregadoDAO

bp_empregados = Blueprint('empregados', __name__, url_prefix='/adm/empregados')


@bp_empregados.route('/atualizar')
def atualizar():
    return render_template('adm/empregados/atualizar.html', empregados=[], filtro_usado='', msg='', css_msg='')


@bp_empregados.route('/roda_atualizar', methods=['POST'])
def roda_atualizar():
    nme_empregado = request.form['nme_empregado']
    filtro_usado = f'Nome do Empregado: {nme_empregado}'
    dao = EmpregadoDAO()
    empregados = dao.read_by_like('nme_empregado', nme_empregado)
    return render_template('adm/empregados/atualizar.html', empregados=empregados, filtro_usado=filtro_usado, msg='', css_msg='')


@bp_empregados.route('/alterar/<int:idt>')
def alterar(idt):
    dao = EmpregadoDAO()
    empregado = dao.read_by_idt(idt)
    if not empregado:
        msg = 'Empregado não encontrado para alteração.'
        css_msg = 'erro'
        return render_template('adm/empregados/atualizar.html', msg=msg, css_msg=css_msg, empregados=[], filtro_usado='')
    return render_template('adm/empregados/alterar.html', empregado=empregado, msg='', css_msg='')


@bp_empregados.route('/salvar_alterar', methods=['POST'])
def salvar_alterar():
    dao = EmpregadoDAO()
    try:
        idt_empregado = int(request.form.get('idt_empregado'))
    except (TypeError, ValueError):
        idt_empregado = None

    empregado = dao.read_by_idt(idt_empregado) if idt_empregado is not None else None
    if not empregado:
        msg = 'Empregado não encontrado para alteração.'
        css_msg = 'erro'
        return render_template('adm/empregados/atualizar.html', msg=msg, css_msg=css_msg, empregados=[], filtro_usado='')

    empregado.nme_empregado = request.form['nme_empregado']
    empregado.eml_empregado = request.form['eml_empregado']
    empregado.sts_empregado = request.form['sts_empregado']

    if dao.update(empregado):
        msg = f"Empregado {empregado.idt_empregado} atualizado com sucesso!"
        css_msg = 'sucesso'
    else:
        msg = 'Erro ao tentar atualizar empregado!'
        css_msg = 'erro'

    return render_template('adm/empregados/alterar.html', empregado=empregado, msg=msg, css_msg=css_msg)


@bp_empregados.route('/excluir/<int:idt>')
def excluir(idt):
    dao = EmpregadoDAO()
    if dao.delete(idt):
        msg = 'Empregado excluído com sucesso!'
        css_msg = "sucesso"
    else:
        msg = 'Falha ao tentar excluir empregado! Verifique se existe alguma pendência!'
        css_msg = "erro"
    setor = dao.read_by_idt(idt)
    return render_template('adm/empregados/atualizar.html', msg=msg, css_msg=css_msg, setores=[], filtro_usado='')

