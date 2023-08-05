"""Este é o modulo "nester.py", e fornece uma função chamada print_lol()
que imprime listar que podem ou não incluir listas aninhadas"""
def print_lol(the_list, level=0):
    """Esta função requer um argumento posicional chamado "the_list), que é
qualquer lista python (de possíveis listas aninhadas). Cada item de dados na
lista fornecida é (recursivamente) impresso na tela em sua própria linha"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end ='')
            print(each_item)
