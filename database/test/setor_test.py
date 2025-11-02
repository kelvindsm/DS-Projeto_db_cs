from database.setor_dao import SetorDAO


def incluir():
    dao = SetorDAO()
    obj = dao.new_object()
    obj.sgl_setor = input("Qual a sigla? ")
    obj.nme_setor = input("Qual o nome? ")
    obj.eml_setor = input("Qual o email? ")
    obj.sts_setor = 'A'
    dao.insert(obj)
    print("Setor incluído:")
    print(obj.idt_setor)


def consultar():
    dao = SetorDAO()
    objs = dao.read_all()
    print("Dados da consulta:")
    for obj in objs:
        print(obj.idt_setor, obj.sgl_setor, obj.nme_setor, obj.eml_setor)


def apagar():
    idt = int(input("Digite o idt do setor: "))
    dao = SetorDAO()
    if dao.delete(idt):
        print('Setor Excluído')
    else:
        print('Erro ao excluir setor')


def filtros():
    campo = input("Qual o campo? ")
    operador = input("Qual o operador? ")
    valor = input("Qual o valor? ")
    dao = SetorDAO()
    objs = dao.read_by_filters([(campo, operador, valor)])
    print("Dados da consulta:")
    for obj in objs:
        print(obj.idt_setor, obj.sgl_setor, obj.nme_setor, obj.eml_setor)


def count():
    dao = SetorDAO()
    num = dao.count()
    print("Numero de objetos setor: ", num)


def sql():
    dao = SetorDAO()
    objs = dao.execute_sql_and_fetch(
        'select nme_setor, sum(vlr_servico) as soma from tt_setor join tb_servico on idt_setor=cod_setor where idt_setor=:idt_setor group by nme_setor',
        {'idt_setor': '1'})
    print("Dados da consulta:")
    for obj in objs:
        print(obj)


if __name__ == '__main__':
    continuar = True
    while (continuar):
        print("""
       1 - Incluir
       2 - Consultar
       3 - Apagar
       4 - Consultar por filtro
       5 - Count
       6 - SQL
       7 - Sair
       """)
        opc = int(input("Quer fazer? "))
        if opc == 1:
            incluir()
        elif opc == 2:
            consultar()
        elif opc == 3:
            apagar()
        elif opc == 4:
            filtros()
        elif opc == 5:
            count()
        elif opc == 6:
            sql()
        elif opc == 7:
            continuar = False
