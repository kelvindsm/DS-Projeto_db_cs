from database.tipo_ocorrencia_dao import TipoOcorrenciaDAO


def incluir():
    dao = TipoOcorrenciaDAO()
    obj = dao.new_object()
    obj.nme_tipo_ocorrencia = input("Qual o nome ocorrencia? ")
    obj.tpo_tipo_ocorrencia = 'E'
    obj.sts_tipo_ocorrencia = 'A'
    obj.txt_modelo_ocorrencia = input("Qual o texto do ocorrencia? ")
    dao.insert(obj)
    print("Ocorrencia incluída:", obj.idt_tipo_ocorrencia)


def listar():
    dao = TipoOcorrenciaDAO()
    lista = dao.read_all()
    for obj in lista:
        print(obj.idt_tipo_ocorrencia, ' - ', obj.nme_tipo_ocorrencia, ' - ', obj.txt_modelo_ocorrencia)


if __name__ == '__main__':
    while True:
        print("""
       1 - Incluir
       2 - Consultar
       3 - Sair
       """)
        opc = int(input("Quer fazer? "))
        if opc == 1:
            incluir()
        elif opc == 2:
            listar()
        elif opc == 3:
            break