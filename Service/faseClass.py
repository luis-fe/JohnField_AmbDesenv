import ConexaoPostgreMPL

class Fase():
    def __init__(self,codFase = None, nomeFase = None) :
        self.codFase = codFase
        self.nomeFase = nomeFase

    def BuscarCodigoFase(self):
        consulta = """
        select
	        "codFase" ,
	        "nomeFase"
        from
	        "Easy"."Fase" f
        where 
            "nomeFase" = %s
        """ 

        conn = ConexaoPostgreMPL.conexaoJohn
        cursor = conn.cursor()
        cursor.execute(consulta,(self.nomeFase))
        consulta = cursor.fetchone()
        self.codFase = consulta[0]
 
        return self.codFase
