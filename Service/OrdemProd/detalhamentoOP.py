import ConexaoPostgreMPL
import pandas as pd
from Service import OP_Tam_Cor_JohnField


def DetalharOPEncerrada(codOP, codCliente):
    chaveOP = str(codOP)+'||'+str(codCliente)
    sql = """
SELECT 
    op."codOP", 
    c."nomeCliente",  
    oe.quantidade,
    op."DataCriacao"::Date, 
    oe.dataencerramento::Date, 
    (oe.dataencerramento::Date - op."DataCriacao"::Date) AS "LeadTime"
FROM "Easy"."OpsEncerradas" oe
INNER JOIN "Easy"."OrdemProducao" op ON op."idOP" = oe."idOP"
INNER JOIN "Easy"."Cliente" c ON c.codcliente = op."codCliente"
WHERE oe."idOP" = %s ;
    """
    conn = ConexaoPostgreMPL.conexaoJohn()
    consulta = pd.read_sql(sql,conn,params=(chaveOP,))
    conn.close()

    detalhaTam = OP_Tam_Cor_JohnField.ConsultaTamCor_OP(codOP,codCliente)
    detalhaTam.drop(['codCliente', 'codOP'], axis=1, inplace=True)

    dados = {
        '0-Numero OP': f'{consulta["codOP"][0]}',
        '1-Cliente': f'{consulta["nomeCliente"][0]}',
        '2-Data Criacao':f'{consulta["DataCriacao"][0]}',
        '3-Data Encerrameto':f'{consulta["dataencerramento"][0]}',
        '4-Lead Time': f'{consulta["LeadTime"][0]} dias',
        '5-Total': f'{consulta["quantidade"][0]} Pçs',
        '6-Detalhamento Grade': detalhaTam.to_dict(orient='records')}

    return pd.DataFrame([dados])
