import pandas as pd
import ConexaoPostgreMPL
import pytz
from Service.Operacoes import Operadores, Opercao
from Service import CategiaJohnField
from datetime import datetime, time, timedelta

def obterHoraAtual():
    fuso_horario = pytz.timezone('America/Sao_Paulo')  # Define o fuso horário do Brasil
    agora = datetime.now(fuso_horario)
    hora_str = agora.strftime('%Y-%m-%d %H:%M:%S')
    return hora_str

def ColetaProducao(codOperador, nomeOperacao, qtdPecas):

    operador = Operadores.ConsultarOperadores()
    print(operador)
    operador = operador[operador['codOperador']==int(codOperador)].reset_index()

    if operador.empty:
        return pd.DataFrame([{'Stauts':False, 'Mensagem':'Operador nao encontrado'}])

    else:

        operacoes =  Opercao.Buscar_Operacoes()
        operacoes = operacoes[operacoes['nomeOperacao']==nomeOperacao].reset_index()

        if operacoes.empty:
            return pd.DataFrame([{'Stauts': False, 'Mensagem': 'Operacoes nao encontrado'}])

        else:
            operacoes = operacoes['codOperacao'][0]
            sql = """
                SELECT 
                    MAX("DataHora"::time) AS "utimoTempo", 
                    COUNT("DataHora") AS registros 
                FROM 
                    "Easy"."RegistroProducao" rp 
                WHERE 
                    "codOperador" = %s
                    AND (("DataHora"::timestamp AT TIME ZONE 'UTC') AT TIME ZONE 'America/Sao_Paulo')::date = (NOW() AT TIME ZONE 'America/Sao_Paulo')::date;
                """
            
            sql2 = """
            SELECT 
                MAX("DataHora"::time) AS "utimoTempo", 
                COUNT("DataHora") AS registros ,
                MAX("DataHora"::varchar) AS "utimaData"
            FROM 
                "Easy"."RegistroProducao" rp 
            WHERE 
                "codOperador" = %s
                AND (("DataHora"::timestamp AT TIME ZONE 'UTC') AT TIME ZONE 'America/Sao_Paulo')::date <= (NOW() AT TIME ZONE 'America/Sao_Paulo')::date;
            """
            conn = ConexaoPostgreMPL.conexaoJohn()
            sql = pd.read_sql(sql, conn, params=(codOperador,))
            sql2 = pd.read_sql(sql2, conn, params=(codOperador,))

            sqlEscala = """
                select "codOperador" , et.periodo1_inicio, periodo2_inicio  , periodo3_inicio, periodo1_fim ,periodo2_fim  from "Easy"."Operador" o 
                inner join "Easy"."EscalaTrabalho" et on et."Escala" = o."Escala" 
                where "codOperador" = %s
                """
            sqlEscala = pd.read_sql(sqlEscala, conn, params=(codOperador,))
            hora_esc1 = sqlEscala['periodo1_inicio'][0]
            hora_esc1Fim = sqlEscala['periodo1_fim'][0]

            hora_esc2 = sqlEscala['periodo2_inicio'][0]
            hora_esc2Fim = sqlEscala['periodo2_fim'][0]

            hora_esc3 = sqlEscala['periodo3_inicio'][0]

            if sql['utimoTempo'][0] == None:
                    ultimotempo = hora_esc1 + ':00'
                    registro = sql['registros'][0] + 1

            else:
                    ultimotempo = sql['utimoTempo'][0]
                    ultimotempo = str(ultimotempo)
                    registro = sql['registros'][0] + 1

            Tempo = obterHoraAtual()
            if not sql2.empty:
                utimaData = sql2['utimaData'][0]
            else:
                utimaData = obterHoraAtual()

            # Converte a string para um objeto datetime
            
            datetime_obj = datetime.strptime(Tempo, "%Y-%m-%d %H:%M:%S")
            ultimotempo = datetime.strptime(ultimotempo, "%H:%M:%S")
            hora_esc1Fim = datetime.strptime(hora_esc1Fim +':00', "%H:%M:%S")
            hora_esc2 = datetime.strptime(hora_esc2 +':00', "%H:%M:%S")
            hora_esc2Fim = datetime.strptime(hora_esc2Fim +':00', "%H:%M:%S")

            hora_esc3 = datetime.strptime(hora_esc3 +':00', "%H:%M:%S")


            # Extrai o componente time do objeto datetime
            HorarioFinal = datetime_obj.time()
            ultimotempo = ultimotempo.time()
            hora_esc1Fim = hora_esc1Fim.time()
            hora_esc2 = hora_esc2.time()
            hora_esc2Fim = hora_esc2Fim.time()
            hora_esc3 = hora_esc3.time()

            intervalo = 0
            if HorarioFinal < hora_esc2:
                    intervalo = 0 + intervalo

            if HorarioFinal > hora_esc2 and ultimotempo < hora_esc2:
                    datetime1 = datetime.combine(datetime.today(), hora_esc1Fim)
                    datetime2 = datetime.combine(datetime.today(), hora_esc2)

                    # Calcula a diferença entre os dois objetos datetime
                    time_difference = datetime2 - datetime1

                    # O resultado é um objeto timedelta
                    # Para obter a diferença em minutos
                    difference_in_minutes = time_difference.total_seconds() / 60
                    intervalo = intervalo + difference_in_minutes

            if HorarioFinal > hora_esc3 and ultimotempo < hora_esc3:

                    datetime1 = datetime.combine(datetime.today(), hora_esc2Fim)
                    datetime2 = datetime.combine(datetime.today(), hora_esc3)

                    # Calcula a diferença entre os dois objetos datetime
                    time_difference = datetime2 - datetime1

                    # O resultado é um objeto timedelta
                    # Para obter a diferença em minutos
                    difference_in_minutes = time_difference.total_seconds() / 60
                    intervalo = intervalo + difference_in_minutes

            inserir = """
                                    insert into "Easy"."RegistroProducao" ("codOperador", "codOperacao", 
                                    "qtdPcs", "DataHora", "HrInico", "HrFim", "desInt", "sequencia", "DiaInicial")
                                    values ( %s, %s , %s ,%s ,%s , %s ,%s ,%s, %s  )
                                    """
            HorarioFinal = HorarioFinal.strftime("%H:%M:%S")

            conn = ConexaoPostgreMPL.conexaoJohn()
            cursor = conn.cursor()
            cursor.execute(inserir, (
                    int(codOperador), int(operacoes), qtdPecas, Tempo, ultimotempo, HorarioFinal, str(intervalo), str(registro),utimaData))
            conn.commit()
            cursor.close()

            conn.close()

            return pd.DataFrame([{'Mensagem': "Registro salvo com Sucesso!", "Status": True, 'teste':f'{sql} , {codOperador}'}])


def ConsultaRegistroPorPeriodo(codOperador, dataInicio, dataFim):
    sql = """
            SELECT * FROM "Easy"."ColetasProducao"
             WHERE
             "Data" >= %s 
             AND "Data" <= %s
             """

    conn = ConexaoPostgreMPL.conexaoJohn()
    consulta = pd.read_sql(sql, conn, params=(dataInicio, dataFim))
    conn.close()

    consulta['tempoTotal(min)'] = consulta['tempoTotal(min)'].round(2)
    consulta['Realizado pcs/Hora'] = 60*(consulta['qtdPcs']/consulta['tempoTotal(min)'])
    consulta['Realizado pcs/Hora'] = consulta['Realizado pcs/Hora'].round(0)
    consulta['Realizado (Efi%)'] = (consulta['Realizado pcs/Hora']/consulta['Meta(pcs/hr)'])*100
    consulta['Realizado (Efi%)'] = consulta['Realizado (Efi%)'].round(2)

    consulta['Realizado (Efi%)'] = consulta['Realizado (Efi%)'].astype(str)+ '%'

    consulta['Data'] = pd.to_datetime(consulta['Data'], format='%a, %d %b %Y %H:%M:%S')
    consulta['Data'] = consulta['Data'].dt.strftime('%d/%m/%Y')

    if codOperador != '':
        consulta = consulta[
            consulta['codOperador'] == int(codOperador)].reset_index()

    # Agregação para contar OPs atrasadas por fase
    Agrupamento = consulta.groupby(['nomeOperacao']).agg({'tempoTotal(min)':'sum','qtdPcs':'sum','Meta(pcs/hr)':'first'}
    ).reset_index()

    Agrupamento['Efi'] = 60*(Agrupamento['qtdPcs']/Agrupamento['tempoTotal(min)'])
    Agrupamento['Efi'] = Agrupamento['Efi'].round(0)
    Agrupamento['Efi'] = (Agrupamento['Efi']/Agrupamento['Meta(pcs/hr)'])*100
    Media = Agrupamento['Efi'].mean()
    Media = round(Media,2)
    dados = {
        '0- Eficiencia Média no dia': f'{Media}% ',
        '2 -DetalhamentoEmAberto': consulta.to_dict(orient='records')}

    return pd.DataFrame([dados])


def ApontamentoParadas(codOperador, Data, InicioAusencia, FimAusencia, motivo, aplicaDesconto):

    VerificaOpeador = Operadores.ConsultarOperadores()
    VerificaOpeador = VerificaOpeador[VerificaOpeador['codOperador']==codOperador].reset_index()

    if VerificaOpeador.empty:
        return pd.DataFrame([{'Status':False, 'Mensagem':'Operador nao encontrado !'}])

    else:
        insert = """
        insert into "Easy"."Paradas"  ("codOperador", "Data", "InicioAusencia", "FimAusencia", "motivo", "aplicaDesconto")
        values ( %s, %s, %s, %s, %s, %s ) 
        """

        InicioAusenciaDate = datetime.strptime(InicioAusencia, "%H:%M")
        FimAusenciaDate = datetime.strptime(FimAusencia, "%H:%M")

        HorarioIni = InicioAusenciaDate.time()
        HorarioFim = FimAusenciaDate.time()

        if HorarioIni > HorarioFim:
            return pd.DataFrame([{'Status': False, 'Mensagem': 'Horario de Inicio é maior que o horario Final !'}])
        else:
            conn = ConexaoPostgreMPL.conexaoJohn()
            cursor = conn.cursor()
            cursor.execute(insert,(codOperador, Data, InicioAusencia, FimAusencia, motivo, aplicaDesconto))
            conn.commit()
            cursor.close()
            conn.close()
            return pd.DataFrame([{'Status': True, 'Mensagem': 'Registro de Parada salvo com sucesso!'}])



def ConsultaPardas(DataInicio, DataFinal):
    sql = """
select p.*, o."nomeOperador"  from "Easy"."Paradas" p 
inner join "Easy"."Operador" o  on o."codOperador" = p."codOperador"  
where p."Data" >= %s and p."Data" <= %s
    """
    conn = ConexaoPostgreMPL.conexaoJohn()
    consulta = pd.read_sql(sql,conn,params=(DataInicio,DataFinal))
    conn.close()
    consulta['Data'] = pd.to_datetime(consulta['Data'], format='%a, %d %b %Y %H:%M:%S %Z')
    consulta['Data'] = consulta['Data'].dt.strftime('%d/%m/%Y')


    return consulta



def ColetaProducaoRetroativa(codOperador, nomeOperacao, qtdPecas, dataRetroativa,HorarioTermino):

    operador = Operadores.ConsultarOperadores()
    print(operador)
    operador = operador[operador['codOperador']==int(codOperador)].reset_index()

    if operador.empty:
        return pd.DataFrame([{'Stauts':False, 'Mensagem':'Operador nao encontrado'}])

    else:

        operacoes =  Opercao.Buscar_Operacoes()
        operacoes = operacoes[operacoes['nomeOperacao']==nomeOperacao].reset_index()

        if operacoes.empty:
            return pd.DataFrame([{'Stauts': False, 'Mensagem': 'Operacoes nao encontrado'}])

        else:
            operacoes = operacoes['codOperacao'][0]

            sql = """SELECT 
            MAX("DataHora"::time) AS "utimoTempo", 
            COUNT("DataHora") AS registros 
            FROM 
            "Easy"."RegistroProducao" rp
            WHERE 
            "codOperador" = %s
            AND "DataHora"::date = %s::date;
                """
            
            sql2 = """
            SELECT 
                MAX("DataHora"::time) AS "utimoTempo", 
                COUNT("DataHora") AS registros ,
                MAX("DataHora"::varchar) AS "utimaData"
            FROM 
                "Easy"."RegistroProducao" rp 
            WHERE 
                "codOperador" = %s
                AND "DataHora"::date <= %s::date;
            """

            conn = ConexaoPostgreMPL.conexaoJohn()
            sql = pd.read_sql(sql, conn, params=(codOperador,dataRetroativa,))
            sql2 = pd.read_sql(sql2, conn, params=(codOperador,dataRetroativa,))

            sqlEscala = """
                select "codOperador" , et.periodo1_inicio, periodo2_inicio  , periodo3_inicio, periodo1_fim ,periodo2_fim  from "Easy"."Operador" o 
                inner join "Easy"."EscalaTrabalho" et on et."Escala" = o."Escala" 
                where "codOperador" = %s
                """
            sqlEscala = pd.read_sql(sqlEscala, conn, params=(codOperador,))
            hora_esc1 = sqlEscala['periodo1_inicio'][0]
            hora_esc1Fim = sqlEscala['periodo1_fim'][0]


            hora_esc2 = sqlEscala['periodo2_inicio'][0]
            hora_esc2Fim = sqlEscala['periodo2_fim'][0]

            hora_esc3 = sqlEscala['periodo3_inicio'][0]

            if sql['utimoTempo'][0] == None:
                    ultimotempo = hora_esc1 + ':00'
                    registro = sql['registros'][0] + 1

            else:
                    ultimotempo = sql['utimoTempo'][0]
                    ultimotempo = str(ultimotempo)
                    registro = sql['registros'][0] + 1

            Tempo = dataRetroativa+' '+HorarioTermino+':00'

            if not sql2.empty:
                utimaData = sql2['utimaData'][0]
            else:
                utimaData = obterHoraAtual()


            # Converte a string para um objeto datetime
            datetime_obj = datetime.strptime(Tempo, "%Y-%m-%d %H:%M:%S")
            ultimotempo = datetime.strptime(ultimotempo, "%H:%M:%S")
            hora_esc1Fim = datetime.strptime(hora_esc1Fim +':00', "%H:%M:%S")
            hora_esc2 = datetime.strptime(hora_esc2 +':00', "%H:%M:%S")
            hora_esc2Fim = datetime.strptime(hora_esc2Fim +':00', "%H:%M:%S")

            hora_esc3 = datetime.strptime(hora_esc3 +':00', "%H:%M:%S")


            # Extrai o componente time do objeto datetime
            HorarioFinal = datetime_obj.time()
            ultimotempo = ultimotempo.time()

            if HorarioFinal < ultimotempo :
                return pd.DataFrame([{'Mensagem': f"Horário Informado {HorarioFinal.strftime('%H:%M')} é menor que o último horário {ultimotempo.strftime('%H:%M')} registrado em {dataRetroativa}", "Status": False, 'Teste': 'falso'}])
            else:    

                hora_esc1Fim = hora_esc1Fim.time()
                hora_esc2 = hora_esc2.time()
                hora_esc2Fim = hora_esc2Fim.time()
                hora_esc3 = hora_esc3.time()

                intervalo = 0
                if HorarioFinal < hora_esc2:
                        intervalo = 0 + intervalo

                if HorarioFinal > hora_esc2 and ultimotempo < hora_esc2:
                        datetime1 = datetime.combine(datetime.today(), hora_esc1Fim)
                        datetime2 = datetime.combine(datetime.today(), hora_esc2)

                        # Calcula a diferença entre os dois objetos datetime
                        time_difference = datetime2 - datetime1

                        # O resultado é um objeto timedelta
                        # Para obter a diferença em minutos
                        difference_in_minutes = time_difference.total_seconds() / 60
                        intervalo = intervalo + difference_in_minutes

                if HorarioFinal > hora_esc3 and ultimotempo < hora_esc3:

                        datetime1 = datetime.combine(datetime.today(), hora_esc2Fim)
                        datetime2 = datetime.combine(datetime.today(), hora_esc3)

                        # Calcula a diferença entre os dois objetos datetime
                        time_difference = datetime2 - datetime1

                        # O resultado é um objeto timedelta
                        # Para obter a diferença em minutos
                        difference_in_minutes = time_difference.total_seconds() / 60
                        intervalo = intervalo + difference_in_minutes

                inserir = """
                                    insert into "Easy"."RegistroProducao" ("codOperador", "codOperacao", 
                                    "qtdPcs", "DataHora", "HrInico", "HrFim", "desInt", "sequencia", "DiaInicial")
                                    values ( %s, %s , %s ,%s ,%s , %s ,%s ,%s, %s  )
                                    """
                HorarioFinal = HorarioFinal.strftime("%H:%M:%S")

                conn = ConexaoPostgreMPL.conexaoJohn()
                cursor = conn.cursor()
                cursor.execute(inserir, (
                        int(codOperador), int(operacoes), qtdPecas, Tempo, ultimotempo, HorarioFinal, str(intervalo), str(registro),utimaData))
                conn.commit()
                cursor.close()

                conn.close()

                return pd.DataFrame([{'Mensagem': "Registro salvo com Sucesso!", "Status": True, 'teste':f'{sql} , {codOperador}'}])