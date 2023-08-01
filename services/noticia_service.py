from bd.bd_aux import BdAux


class NoticiaService:
    def __init__(self):
        pass

    @staticmethod
    def inserir_resultado_noticia(resultado, link, fonte=None, titulo=None):
        query = 'EXEC SP_INSERIR_RESULTADO_ANALISE ?, ?'

        args = [resultado, link]

        if fonte is not None:
            args.append(fonte)

        if titulo is not None and fonte is not None:
            args.append(titulo)
        elif titulo is not None and fonte is None:
            args.append('')
            args.append(titulo)

        bd_aux = BdAux()
        bd_aux.executar_query(query, args)
        bd_aux.desconectar()
