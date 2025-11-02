from flask import Blueprint, render_template, request

from database.setor_dao import SetorDAO
from database.servico_dao import ServicoDAO

bp_servicos = Blueprint('servicos', __name__, url_prefix='/adm/servicos')


@bp_servicos.route('/incluir')  # /adm/servicos/incluir
def incluir():
    dao = SetorDAO()
    lst_setores = dao.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/servicos/incluir.html', msg="", css_msg="", lst_setores=lst_setores)


@bp_servicos.route('/salvar_incluir', methods=['POST'])  # /adm/servicos/salvar_incluir
def salvar_incluir():
    dao = ServicoDAO()
    serv = dao.new_object()
    serv.nme_servico = request.form['nme_servico']
    serv.num_dias_servico = int(request.form['num_dias_servico'])
    serv.vlr_servico = request.form['vlr_servico']
    serv.txt_modelo_servico = request.form['txt_modelo_servico']
    serv.sts_servico = request.form['sts_servico']
    serv.cod_setor = int(request.form['cod_setor'])

    if dao.insert(serv):
        msg = f"Serviço número {serv.idt_servico} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir serviço!"
        css_msg = "erro"

    dao_setor = SetorDAO()
    lst_setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])

    return render_template('adm/servicos/incluir.html', msg=msg, css_msg=css_msg, lst_setores=lst_setores)


@bp_servicos.route('/consultar')  # /adm/servicos/consultar
def consultar():
    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/servicos/consultar.html', servicos=[], setores=setores, filtro_usado='')


@bp_servicos.route('/roda_consultar', methods=['POST'])  # /adm/servicos/rodar_consultar
def roda_consultar():
    nme_servico = request.form['nme_servico']
    cod_setor = request.form['cod_setor']
    filtros = []
    if nme_servico:
        filtros.append(('nme_servico', 'ilike', f'%{nme_servico}%'))
    if cod_setor:
        filtros.append(('cod_setor', '=', int(cod_setor)))
    filtro_usado = f'Nome do Serviço: {nme_servico or "Não informado"} / Código do Setor: {cod_setor or "Todos"}'

    dao = ServicoDAO()
    servicos = dao.read_by_filters(filtros)

    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/servicos/consultar.html', servicos=servicos, setores=setores, filtro_usado=filtro_usado)


@bp_servicos.route('/atualizar')  # /adm/servicos/atualizar
def atualizar():
    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/servicos/atualizar.html', servicos=[], setores=setores, filtro_usado='')


@bp_servicos.route('/roda_atualizar', methods=['POST'])  # /adm/servicos/rodar_atualizar
def roda_atualizar():
    nme_servico = request.form['nme_servico']
    cod_setor = request.form['cod_setor']
    filtros = []
    if nme_servico:
        filtros.append(('nme_servico', 'ilike', f'%{nme_servico}%'))
    if cod_setor:
        filtros.append(('cod_setor', '=', int(cod_setor)))
    filtro_usado = f'Nome do Serviço: {nme_servico or "Não informado"} / Código do Setor: {cod_setor or "Todos"}'

    dao = ServicoDAO()
    servicos = dao.read_by_filters(filtros)

    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/servicos/atualizar.html', servicos=servicos, setores=setores, filtro_usado=filtro_usado)


@bp_servicos.route('/alterar/<int:idt>')  # /adm/servicos/alterar/<idt>
def alterar(idt):
    dao_servico = ServicoDAO()
    servico = dao_servico.read_by_idt(idt)
    if not servico:
        msg = 'Serviço não encontrado para alteração.'
        css_msg = 'erro'
        dao_setor = SetorDAO()
        setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
        return render_template('adm/servicos/atualizar.html', msg=msg, css_msg=css_msg, servicos=[], setores=setores, filtro_usado='')

    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/servicos/alterar.html', servico=servico, setores=setores, msg="", css_msg="")


@bp_servicos.route('/salvar_alterar', methods=['POST'])  # /adm/servicos/salvar_alterar
def salvar_alterar():
    dao_servico = ServicoDAO()

    try:
        idt_servico = int(request.form.get('idt_servico'))
    except (TypeError, ValueError):
        idt_servico = None

    servico = dao_servico.read_by_idt(idt_servico) if idt_servico is not None else None
    if not servico:
        msg = 'Serviço não encontrado para alteração.'
        css_msg = 'erro'
        dao_setor = SetorDAO()
        setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
        return render_template('adm/servicos/atualizar.html', msg=msg, css_msg=css_msg, servicos=[], setores=setores, filtro_usado='')

    servico.nme_servico = request.form['nme_servico']
    servico.num_dias_servico = int(request.form['num_dias_servico'])
    servico.vlr_servico = request.form['vlr_servico']
    servico.txt_modelo_servico = request.form['txt_modelo_servico']
    servico.sts_servico = request.form['sts_servico']
    servico.cod_setor = int(request.form['cod_setor'])

    if dao_servico.update(servico):
        msg = f"Serviço {servico.idt_servico} atualizado com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar atualizar serviço!"
        css_msg = "erro"

    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/servicos/alterar.html', servico=servico, setores=setores, msg=msg, css_msg=css_msg)


@bp_servicos.route('/excluir/<int:idt>')
def excluir(idt):
    dao = ServicoDAO()
    if dao.delete(idt):
        msg = 'Serviço excluído com sucesso!'
        css_msg = "sucesso"
    else:
        msg = 'Falha ao tentar excluir serviço! Verifique se existe alguma dependência!'
        css_msg = "erro"
    setor = dao.read_by_idt(idt)
    return render_template('adm/servicos/atualizar.html', msg=msg, css_msg=css_msg, setores=[], filtro_usado='')