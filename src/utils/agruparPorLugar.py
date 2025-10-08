def agrupar(casas):
    agrupadas={}
    for casa in casas:
        #titulo=casa.title.rsplit(", ", 1)[-1]
        if  casa.title not in agrupadas:
            print(casa.title)
            agrupadas[casa.title]=[]
        agrupadas[casa.title].append(casa)
    return agrupadas
