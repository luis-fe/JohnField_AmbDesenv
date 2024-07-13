'''
Relatorio criado para obter as ops baixadas no periodo
'''
import pandas as pd
import ConexaoPostgreMPL

def RelatorioEncerramento(dataInicio, dataFinal):
    consulta  ="""
    select "idOP", dataencerramento::varchar as dataencerramento, u."nomeUsuario" as usuario_encerramento  from railway."Easy"."OpsEncerradas" oe
    inner join "Easy"."Usuario" u on u.idusuario = oe.usuario_encerramento
    where dataencerramento >= %s and dataencerramento <=%s
    """

    consulta2 = """
    select * from railway."Easy"."DetalhaOP" do2 
    """

    with ConexaoPostgreMPL.conexaoJohn() as conn:
        consulta = pd.read_sql(consulta,conn,params=(dataInicio,dataFinal,))
        consulta2 = pd.read_sql(consulta2,conn)

        consulta = pd.merge(consulta,consulta2,on='idOP',how='left')

    consulta['dataencerramento'] = consulta['dataencerramento'].apply(converterData)

    qtd = consulta['']
    dados = {
        '0- Qtde Peças': f'{Media}% ',
        '2 -Detalhamento': consulta.to_dict(orient='records')}

    return pd.DataFrame([dados])
def converterData(date_str):
    year = date_str[:4]
    month = date_str[5:7]
    day = date_str[8:]
    return f"{day}/{month}/{year}"