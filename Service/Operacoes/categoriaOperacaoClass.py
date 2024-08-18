import ConexaoPostgreMPL

class CategoriaOperacao():
    def __init__(self,codCategoriaOperacao=None, nomeCategoriaOperacao = None) :
        self.codCategoriaOperacao = codCategoriaOperacao 
        self.nomeCategoriaOperacao = nomeCategoriaOperacao 

    def BuscarCodigoCategoria(self):
        consulta = """
select
	c.id_categoria,
	nomecategoria ,
	metadiaria
from
	"Easy".categoriaoperacao c
        where 
            "nomecategoria" = %s
        """ 

        conn = ConexaoPostgreMPL.conexaoJohn
        cursor = conn.cursor()
        cursor.execute(consulta,(self.nomeCategoriaOperacao))
        consulta = cursor.fetchone()
        self.codCategoriaOperacao = consulta[0]
 
        return self.codCategoriaOperacao