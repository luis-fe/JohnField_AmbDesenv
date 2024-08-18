import pandas as pd
import ConexaoPostgreMPL

class Produtividade():
    def __init__(self, dataInicio = None, dataFinal =None):
        self.dataInicio = dataInicio
        self.dataFinal = dataFinal

    def ProdutividadePorCategoriaOperacao(self):
        sql = """
        select
	        co.nomecategoria,
	        max(co.metadiaria) as "MetaDia",
	        sum(cp."qtdPcs") as "Realizado"
        from
	        "Easy".categoriaoperacao co
        inner join "Easy"."Operacao" o on
	        o.categoriaoperacao = id_categoria::Varchar
        inner join "Easy"."ColetasProducao" cp on
	        cp."nomeOperacao" = o."nomeOperacao"
        where
	        cp."Data" >= %s and cp."Data" <= %s 
        group by
	        co.nomecategoria
        """
        conn = ConexaoPostgreMPL.conexaoEngine()
        consulta = pd.read_sql(sql,conn,params=(self.dataInicio, self.dataFinal))
        consulta['Realizado%'] = consulta['Realizado'] / consulta['MetaDia']
        consulta['Realizado%'] = consulta['Realizado%'].round()
        return consulta