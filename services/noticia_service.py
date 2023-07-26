from bd.bd_aux import BdAux


class NoticiaService:
    def __init__(self):
        pass

    @staticmethod
    def inserir_resultado_noticia(resultado, link):
        query = 'EXEC SP_INSERIR_RESULTADO_ANALISE ?, ?'

        bd_aux = BdAux()
        bd_aux.executar_query(query, resultado, link)
        bd_aux.desconectar()
