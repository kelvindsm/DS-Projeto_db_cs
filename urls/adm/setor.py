from flask import Blueprint, render_template, request
from database.setor_dao import SetorDAO

bp_setor = Blueprint('setor', __name__, url_prefix='/adm/setor')


@bp_setor.route('/incluir')  # /adm/setor/incluir
def incluir():
    return render_template('adm/setor/incluir.html', msg="", css_msg="")


@bp_setor.route('/salvar_incluir', methods=['POST'])  # /adm/setor/salvar_incluir
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


@bp_setor.route('/consultar')  # /adm/setor/consultar
def consultar():
    return render_template('adm/setor/consultar.html', setores=[], filtro_usado='')


@bp_setor.route('/roda_consultar', methods=['POST'])  # /adm/setor/roda_consultar
def roda_consultar():
    nme_setor = request.form['nme_setor']
    filtro_usado = f'Nome do Setor: {nme_setor}'
    dao = SetorDAO()
    setores = dao.read_by_like('nme_setor', nme_setor)
    return render_template('adm/setor/consultar.html', setores=setores, filtro_usado=filtro_usado)


@bp_setor.route('/atualizar')  # /adm/setor/atualizar
def atualizar():
    return render_template('adm/setor/atualizar.html', setores=[], filtro_usado='')


@bp_setor.route('/roda_atualizar', methods=['POST'])  # /adm/setor/rodar_atualizar
def roda_atualizar():
    nme_setor = request.form['nme_setor']
    filtro_usado = f'Nome do Setor: {nme_setor}'
    dao = SetorDAO()
    setores = dao.read_by_like('nme_setor', nme_setor)
    return render_template('adm/setor/atualizar.html', setores=setores, filtro_usado=filtro_usado)


@bp_setor.route('/alterar/<int:idt>')  # /adm/setor/alterar/<idt>
def alterar(idt):
    dao = SetorDAO()
    setor = dao.read_by_idt(idt)
    if not setor:
        msg = 'Setor não encontrado para alteração.'
        css_msg = 'erro'
        return render_template('adm/setor/atualizar.html', msg=msg, css_msg=css_msg, setores=[], filtro_usado='')
    return render_template('adm/setor/alterar.html', setor=setor, msg="", css_msg="")


@bp_setor.route('/salvar_alterar', methods=['POST'])  # /adm/setor/salvar_alterar
def salvar_alterar():
    dao = SetorDAO()
    try:
        idt_setor = int(request.form.get('idt_setor'))
    except (TypeError, ValueError):
        idt_setor = None

    setor = dao.read_by_idt(idt_setor) if idt_setor is not None else None
    if not setor:
        msg = 'Setor não encontrado para alteração.'
        css_msg = 'erro'
        return render_template('adm/setor/atualizar.html', msg=msg, css_msg=css_msg, setores=[], filtro_usado='')

    setor.sgl_setor = request.form['sgl_setor']
    setor.nme_setor = request.form['nme_setor']
    setor.eml_setor = request.form['eml_setor']
    setor.sts_setor = request.form['sts_setor']

    if dao.update(setor):
        msg = f"Setor {setor.idt_setor} atualizado com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar atualizar setor!"
        css_msg = "erro"

    return render_template('adm/setor/alterar.html', setor=setor, msg=msg, css_msg=css_msg)


@bp_setor.route('/excluir/<int:idt>')
def excluir(idt):
    dao = SetorDAO()
    if dao.delete(idt):
        msg = 'Setor excluído com sucesso!'
        css_msg = "sucesso"
    else:
        msg = 'Falha ao tentar excluir setor! Verifique se existe alguma dependência!'
        css_msg = "erro"
    setor = dao.read_by_idt(idt)
    return render_template('adm/setor/atualizar.html', msg=msg, css_msg=css_msg, setores=[], filtro_usado='')