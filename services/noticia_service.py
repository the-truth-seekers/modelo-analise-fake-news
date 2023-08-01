from bd.bd_aux import BdAux


class NoticiaService:
    def __init__(self):
        pass

    @staticmethod
    def inserir_resultado_noticia(resultado, link, fonte='', titulo=''):
        query = 'EXEC SP_INSERIR_RESULTADO_ANALISE ?, ?, ?, ?'

        args = [resultado, link, fonte, titulo]

        bd_aux = BdAux()
        bd_aux.executar_query(query, args)
        bd_aux.desconectar()
