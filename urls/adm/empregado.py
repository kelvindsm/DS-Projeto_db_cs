from flask import Blueprint, render_template, request

from database.Empregado_dao import EmpregadoDAO
from database.Local_dao import LocalDAO

bp_empregados = Blueprint('empregados', __name__, url_prefix='/adm/empregados')

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
    nme_empregado = request.form.get('nme_empregado', '').strip()
    cod_local = request.form.get('cod_local', '').strip()
    filtros = []

    if nme_empregado:
        filtros.append(('nme_empregado', 'ilike', f'%{nme_empregado}%'))
    if cod_local:
        filtros.append(('cod_local', '=', int(cod_local)))

    filtro_usado = f'Nome do Empregado: {nme_empregado or "Não informado"} / Código do Local: {cod_local or "Todos"}'

    # filtro_usado = f'Nome do empregado: {nme_empregado}'
    dao = EmpregadoDAO()
    empregados = dao.read_by_filters(filtros)

    dao_local = LocalDAO()
    locais = dao_local.read_by_filters([('sts_local', '=', 'A')])

    return render_template('adm/empregados/consultar.html', empregados=empregados, locais=locais, filtro_usado=filtro_usado)

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
    empregado = dao.read_by_idt(idt)
    return render_template('adm/empregados/atualizar.html', msg=msg, css_msg=css_msg, empregados=[], filtro_usado='')
