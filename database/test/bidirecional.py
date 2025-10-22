from database.setor_dao import SetorDAO
from database.servico_dao import ServicoDAO


def lista_setor_servicos():
    dao = SetorDAO()
    lista = dao.read_all()
    for setor in lista:
        print(setor.sgl_setor, setor.nme_setor)
        for servico in setor.tb_servico_collection:
            print('>>>', servico.nme_servico, servico.vlr_servico)


def lista_servicos():
    dao = ServicoDAO()
    lista = dao.read_all()
    for servico in lista:
        print(servico.tt_setor.sgl_setor, servico.tt_setor.nme_setor, servico.nme_servico, servico.vlr_servico)


if __name__ == '__main__':
    lista_setor_servicos()
    print('-' * 30)
    lista_servicos()
