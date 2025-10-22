from database.setor_dao import SetorDAO

print("Incluir novo setor")
sigla = input("Qual a sigla do setor? ")
nome = input("Qual o nome do setor? ")
email = input("Qual o email do setor? ")
status = input("Qual o status do setor? ")

dao = SetorDAO()
setor = dao.new_object()
setor.sgl_setor = sigla
setor.nme_setor = nome
setor.eml_setor = email
setor.sts_setor = status

dao.insert(setor)
print(f"Setor {setor.idt_setor} incluido com sucesso")