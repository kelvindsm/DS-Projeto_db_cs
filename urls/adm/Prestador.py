from flask import Blueprint, render_template, request

from database.Prestador_dao import PrestadorDAO
from database.setor_dao import SetorDAO

bp_prestadores = Blueprint('prestadores', __name__, url_prefix='/adm/prestadores')

@bp_prestadores.route('/incluir')
def incluir():
    dao = SetorDAO()
    lst_setores = dao.read_by_filters([('sts_setor', '=', 'A')]) or []

    return render_template('adm/prestadores/incluir.html', msg="", css_msg="", lst_setores=lst_setores)
@bp_prestadores.route('/salvar_incluir', methods=['POST'])  # /adm/prestadores/incluir
def salvar_incluir():
    dao = PrestadorDAO()
    prestadores = dao.new_object()
    prestadores.nme_prestador = request.form['nme_prestador']
    prestadores.eml_prestador = request.form['eml_prestador']
    prestadores.sts_prestador = request.form['sts_prestador']
    prestadores.cod_setor = request.form['cod_setor']
    prestadores.mat_prestador = request.form['mat_prestador']
    prestadores.tel_prestador = request.form['tel_prestador']
    prestadores.rml_prestador = request.form['rml_prestador']
    prestadores.pwd_prestador = request.form['pwd_prestador']

    if dao.insert(prestadores):
        msg = f"Prestador número {prestadores.idt_prestador} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir prestador!"
        css_msg = "erro"

    dao_setor = SetorDAO()
    lst_setores = dao_setor.read_by_filters([('sts_prestador', '=', 'A')]) or []

    return render_template('adm/prestadores/incluir.html', msg=msg, css_msg=css_msg, lst_setores=lst_setores)

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

