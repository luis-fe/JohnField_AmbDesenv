import pandas as pd
import ConexaoPostgreMPL
from datetime import datetime

class Produtividade():
    def __init__(self, dataInicio = None, dataFinal =None):
        self.dataInicio = dataInicio
        self.dataFinal = dataFinal
        self.codOperador = None 
        self.codregistro= None

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

        #Implementar o Numerero de Operadores que realizacao a funcao no dia
        consulta2 = pd.read_sql(sql2,conn,params=(self.dataInicio, self.dataFinal))
        consulta2['QtdOperadores'] = 1
        consulta2 = consulta2.groupby(['nomecategoria']).agg(
        QtdOperadores=('QtdOperadores', 'sum')).reset_index()
        consulta =pd.merge(consulta, consulta2, on = 'nomecategoria', how='left')


        consulta['Realizado%'] = (consulta['Realizado'] / consulta['MetaDia'])*100
        consulta['Realizado%'] = consulta['Realizado%'].round(1)

        return consulta
    

    def CalcularTempo(self, InicioOperacao, FimOperacao, tempoInicio, tempoFim, codOperador, codRegistro):
    # Converte as datas de início e fim em objetos datetime se forem strings
        if isinstance(InicioOperacao, str):
            InicioOperacao = datetime.strptime(InicioOperacao, "%Y-%m-%d")
        if isinstance(FimOperacao, str):
            FimOperacao = datetime.strptime(FimOperacao, "%Y-%m-%d")
    
        # Converte as horas de início e fim em objetos datetime
        tempoInicio = datetime.strptime(tempoInicio, "%H:%M:%S")
        tempoFim = datetime.strptime(tempoFim, "%H:%M:%S")


        # Agora podemos gerar uma sequência de datas
        try:
            datas = pd.date_range(start=InicioOperacao, end=FimOperacao)
        except ValueError as e:
            raise ValueError(f"Erro ao gerar o range de datas: {e},inico operacao{InicioOperacao},fim{FimOperacao}")

        # Verifica se há algum domingo na sequência de datas
        tem_domingo = any(date.weekday() == 6 for date in datas)

        delta_dias = (FimOperacao - InicioOperacao).days
        #self.codOperador = codOperador
        #self.codregistro = codRegistro
        #self.AtualizarValores(delta_dias)

        if InicioOperacao == FimOperacao:
            # Calcular a diferença entre os horários
            delta = tempoFim - tempoInicio
            return delta.total_seconds() / 60
    
        elif delta_dias == 1:
            tempoFImEscala = "17:30:00"
            tempoInicioEscala = "07:30:00"
            tempoFImEscala = datetime.strptime(tempoFImEscala, "%H:%M:%S")
            tempoInicioEscala = datetime.strptime(tempoInicioEscala, "%H:%M:%S")

            delta1 = tempoFImEscala - tempoInicio
            delta2 = tempoFim - tempoInicioEscala
        
            delta = delta1.total_seconds() + delta2.total_seconds()
        
            return delta / 60

        elif (delta_dias == 3 or delta_dias == 2 ) and tem_domingo:
            tempoFImEscala = "16:20:00"
            tempoInicioEscala = "07:30:00"
            tempoFImEscala = datetime.strptime(tempoFImEscala, "%H:%M:%S")
            tempoInicioEscala = datetime.strptime(tempoInicioEscala, "%H:%M:%S")

            delta1 = tempoFImEscala - tempoInicio
            delta2 = tempoFim - tempoInicioEscala
        
            delta = delta1.total_seconds() + delta2.total_seconds()
        
            return delta/ 60
        else:
            # Se as datas forem diferentes e não forem tratadas acima
            # Calcular a diferença entre os horários
            delta = tempoFim - tempoInicio
            return delta.total_seconds() / 60
        
    def ProdutividadeOperadores(self):

        sql = """
        SELECT
            "Codigo Registro",
            "Data"::Date,
            case when "DiaInicial" is null then "Data"::Date else  "DiaInicial"::Date end "DiaInicial",
            "Hr Inicio",
            "Hr Final",
            "codOperador",
            "nomeOperador",
            "nomeOperacao",
            "paradas min",
            "tempoTotal(min)",
            "qtdPcs",
            "Meta(pcs/hr)"
        FROM
            "Easy"."ColetasProducao" cp
        WHERE
            "Data" >= %s AND "Data" <= %s
        ORDER BY
            "Data", "codOperador", "Codigo Registro"
        """

        conn = ConexaoPostgreMPL.conexaoEngine()
        produtividade = pd.read_sql(sql, conn, params=(self.dataInicio, self.dataFinal))

        if produtividade.empty:
            return pd.DataFrame([])

        else:
        # Adicionar uma coluna calculada usando a função CalcularTempo
            produtividade['TempoRealizado(Min)'] = produtividade.apply(
            lambda row: self.CalcularTempo(
            row['DiaInicial'], row['Data'], row['Hr Inicio'], row['Hr Final'],row['codOperador'],
            row['Codigo Registro']
        ), axis=1)


            produtividade['tempoTotal(min)Acum'] = produtividade.groupby(['Data', 'codOperador'])[
                'tempoTotal(min)'].cumsum()
            produtividade['tempo Previsto'] = produtividade['qtdPcs'] / round(produtividade['Meta(pcs/hr)'] / 60, 2)
            produtividade['tempo PrevistoAcum'] = produtividade.groupby(['Data', 'codOperador'])[
                'tempo Previsto'].cumsum()
            produtividade['tempo PrevistoAcum'] = produtividade['tempo PrevistoAcum'].round(2)
            produtividade['qtdPcsAcum'] = produtividade.groupby(['Data', 'codOperador'])['qtdPcs'].cumsum()

            consulta = produtividade.groupby(['Data', 'codOperador']).agg({
                "Codigo Registro": 'max'}).reset_index()

            consulta = pd.merge(consulta, produtividade, on=['Data', 'codOperador', 'Codigo Registro'])
            consulta = consulta.drop_duplicates()

            consulta['Eficiencia'] = round(consulta['tempo PrevistoAcum'] / consulta['tempoTotal(min)Acum'], 3) * 100
            consulta['Eficiencia'] = consulta['Eficiencia'].round(1)

            consulta2 = consulta.groupby('codOperador').agg({
                'nomeOperador': 'first',
                'qtdPcsAcum': 'sum',
                'tempo PrevistoAcum': 'sum',
                'tempoTotal(min)Acum': 'sum'
            }).reset_index()

            consulta2['tempoTotal(min)Acum'] = consulta2['tempoTotal(min)Acum'].round(4)
            consulta2['Eficiencia'] = round(consulta2['tempo PrevistoAcum'] / consulta2['tempoTotal(min)Acum'], 3) * 100
            consulta2['Eficiencia'] = consulta2['Eficiencia'].round(1)

            consulta2 = consulta2.sort_values(by=['Eficiencia'], ascending=False)
            consulta2['Eficiencia'] = consulta2['Eficiencia'].astype(str) + '%'

            efiMedia = round(consulta2['tempo PrevistoAcum'].sum() / consulta2['tempoTotal(min)Acum'].sum(), 3) * 100

            dados = {
                '0-Eficiencia Média Periodo': f'{efiMedia}%',
                '1-Detalhamento': consulta2.to_dict(orient='records')}

            return pd.DataFrame([dados])
        
    def AtualizarValores(self,dia_entreData):
    
        insert = """update "Easy"."RegistroProducao" set "dia_entre_datas" = %s
         where "codOperador" = %s and "sequencia" = %s """
                    
        with ConexaoPostgreMPL.conexaoJohn() as conn:
            with conn.cursor() as curr:
                curr.execute(insert,(dia_entreData, self.codOperador, self.codregistro))
                conn.commit()




