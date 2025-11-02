from database.servico_dao import ServicoDAO


def incluir():
    dao = ServicoDAO()
    obj = dao.new_object()
    obj.nme_servico = input("Qual o nome? ")
    obj.num_dias_servico = int(input("Número de dias serviço? "))
    obj.vlr_servico = float(input("Qual o valor do serviço? "))
    obj.txt_modelo_servico = input("Qual o texto modelo do serviço? ")
    obj.cod_setor = int(input("Qual o código do setor do serviço? "))
    obj.sts_servico = 'A'
    dao.insert(obj)
    print("Servico incluído:")
    print(obj.idt_servico)


def consultar():
    dao = ServicoDAO()
    objs = dao.read_all()
    print("Dados da consulta:")
    for obj in objs:
        print(("IDT do serviço: ", obj.idt_servico, " | Nome do serviço: ",obj.nme_servico,
              " | Numero de dias: ", obj.num_dias_servico, " | Valor da diária: ",obj.vlr_servico,
              " | Texto modelo do serviço: ", obj.txt_modelo_servico,
              " | Status do serviço: ", obj.sts_servico, " | Código do setor: ",obj.cod_setor))

        # print(obj.idt_servico, obj.nme_servico, obj.num_dias_servico, obj.vlr_servico, obj.txt_modelo_servico,
        #       obj.sts_servico, obj.cod_setor)


def apagar():
    idt = int(input("Digite o idt do Servico: "))
    dao = ServicoDAO()
    if dao.delete(idt):
        print('Servico Excluído')
    else:
        print('Erro ao excluir Servico')


def filtros():
    campo = input("Qual o campo? ")
    operador = input("Qual o operador? ")
    valor = input("Qual o valor? ")
    dao = ServicoDAO()
    objs = dao.read_by_filters([(campo, operador, valor)])
    print("Dados da consulta:")
    for obj in objs:
        print("IDT do serviço: ", obj.idt_servico, " | Nome do serviço: ",obj.nme_servico,
              " | Numero de dias: ", obj.num_dias_servico, " | Valor da diária: ",obj.vlr_servico,
              " | Texto modelo do serviço: ", obj.txt_modelo_servico,
              " | Status do serviço: ", obj.sts_servico, " | Código do setor: ",obj.cod_setor)


def count():
    dao = ServicoDAO()
    num = dao.count()
    print("Numero de objetos servico: ", num)


def sql():
    dao = ServicoDAO()
    objs = dao.execute_sql_and_fetch(
        'select nme_setor, count(idt_servico) as conta from tt_setor left join tb_servico on idt_setor=cod_setor group by nme_setor')
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
