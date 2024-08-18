import pandas as pd
import ConexaoPostgreMPL
from Service import FaseJohnField, CategiaJohnField

def Buscar_Operacoes():
    print('meu teste')
    conn = ConexaoPostgreMPL.conexaoEngine()

    sql = """
	            select  c.*,c2."nomecategoria" as "nomeCategoria"  ,to2."tempoPadrao" as "TempoPadrao(s)", f."nomeFase", "Maq/Equipamento"  from "Easy"."Operacao" c
        inner join "Easy"."Fase" f on f."codFase" = c."codFase"
        inner join "Easy"."TemposOperacao" to2 on to2."codOperacao" = c."codOperacao" 
        left join "Easy"."categoriaoperacao" c2 on c2.id_categoria::varchar = c."categoriaoperacao"  
    """

    consulta = pd.read_sql(sql,conn)

    consulta['Pcs/Hora'] = (60*60)/consulta['TempoPadrao(s)']
    consulta['Pcs/Hora'] = consulta['Pcs/Hora'].astype(int)
    print(consulta)

    return consulta