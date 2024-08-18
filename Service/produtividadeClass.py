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

        sql2 = """
        	select
	            co.nomecategoria, cp."nomeOperador" 
            from 
	            "Easy".categoriaoperacao co
            inner join "Easy"."Operacao" o on
	            o.categoriaoperacao = id_categoria::Varchar
            inner join "Easy"."ColetasProducao" cp on
	            cp."nomeOperacao" = o."nomeOperacao"
            where
	        cp."Data" >= %s and cp."Data" <= %s 
            group by
	            co.nomecategoria, cp."nomeOperador" 
        """
        conn = ConexaoPostgreMPL.conexaoEngine()
        consulta = pd.read_sql(sql,conn,params=(self.dataInicio, self.dataFinal))
        consulta2 = pd.read_sql(sql2,conn,params=(self.dataInicio, self.dataFinal))
        consulta2['QtdOperadores'] = 1
        consulta2 = consulta2.groupby(['nomecategoria']).agg(
        quantidadeOP=('QtdOperadores'),quantidadePc=('sum')).reset_index()
        consulta =pd.merge(consulta, consulta2, on = 'nomecategoria', how='left')

        consulta['Realizado%'] = (consulta['Realizado'] / consulta['MetaDia'])*100
        consulta['Realizado%'] = consulta['Realizado%'].round(1)

        #Implementar o Numerero de Operadores que realizacao a funcao no dia
        return consulta