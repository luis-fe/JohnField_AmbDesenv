import ConexaoPostgreMPL
import pandas as pd

def ConsultarOperadores():
    sql = """
    select * from "Easy"."Operador" o 
    """

    conn = ConexaoPostgreMPL.conexaoJohn()
    consulta = pd.read_sql(sql,conn)
    conn.close()

    return consulta

def InserirOperador(codOperador, nomeOperador, EscalaTrabalho):
    # Verificando se existe o operador
    verifica = ConsultarOperadores()
    verifica1 = verifica[verifica['codOperador']== codOperador].reset_index()

    if not verifica1.empty:
        return pd.DataFrame([{'Mensagem': "codOperador ja existe", "status": False}])
    else:
        verifica2 = verifica[verifica['nomeOperador']== nomeOperador].reset_index()

        if not verifica2.empty:
            return pd.DataFrame([{'Mensagem': "nome do Operdaror  ja existe", "status": False}])

        else:
            verificaEscala = ConsultaEscalaTrabalho()
            verificaEscala = verificaEscala[verificaEscala["Escala"]==EscalaTrabalho].reset_index()

            if verificaEscala.empty:
                return pd.DataFrame([{'Mensagem': "Escala de trabalho nao encontrada", "status": False}])
            else:
                insert = """
                insert into "Easy"."Operador" 
                ("codOperador", "nomeOperador", "Escala") values (%s , %s , %s) 
                """
                conn = ConexaoPostgreMPL.conexaoJohn()
                cur = conn.cursor()
                cur.execute(insert, (int(codOperador), nomeOperador, EscalaTrabalho))
                conn.commit()
                cur.close()
                conn.close()

                return pd.DataFrame([{'Mensagem': "Operdaror inserido com Sucesso", "status": True}])


def AtualizandoOperador(codOperador, nomeOperador, Escala):
    # Verificando se existe o operador
    verifica = ConsultarOperadores()
    verifica1 = verifica[verifica['codOperador']== codOperador].reset_index()

    if  verifica1.empty:
        return pd.DataFrame([{'Mensagem': "codOperador nao existe", "status": False}])

    else:

        if nomeOperador == '-':
            nomeOperador = verifica1['nomeOperador'][0]

        if Escala == '-':
            Escala = verifica1['Escala'][0]




        update = """
            update "Easy"."Operador"
            set "nomeOperador" = %s , "Escala" = %s
            where "codOperador" = %s
            """
        conn = ConexaoPostgreMPL.conexaoJohn()
        cur = conn.cursor()
        cur.execute(update, (nomeOperador,Escala, int(codOperador)))
        conn.commit()
        cur.close()
        conn.close()

        return pd.DataFrame([{'Mensagem': "Operdaror alterado com Sucesso", "status": True}])

def ConsultaEscalaTrabalho():

    sql = """
    select "Escala", "des_periodo1" as "descricaoPeriodo1", "periodo1_inicio" as "inicio_periodo1" ,"periodo1_fim" as "termino_periodo1",
    "des_periodo2" as "descricaoPeriodo2", "periodo2_inicio" as "inicio_periodo2" ,"periodo2_fim" as "termino_periodo2",
    "des_periodo3" as "descricaoPeriodo3", "periodo3_inicio" as "inicio_periodo3" ,"periodo3_fim" as "termino_periodo3"
    from "Easy"."EscalaTrabalho" 
    """

    conn = ConexaoPostgreMPL.conexaoJohn()
    consulta = pd.read_sql(sql,conn)
    conn.close()

    return consulta

def InserirEscalaTrabalho(nomeEscala, descricaoPeriodo1 , inicio_periodo1, termino_periodo1,
                          descricaoPeriodo2 , inicio_periodo2, termino_periodo2,
                          descricaoPeriodo3 , inicio_periodo3, termino_periodo3):

    # Verifica se existe a escala informada
    verfica = ConsultaEscalaTrabalho()
    verfica = verfica[verfica["Escala"]==nomeEscala].reset_index()

    if not verfica.empty:
        return pd.DataFrame([{'Mensagem': "Escala de Trabalho ja existe", "status": False}])
    else:

        insert = """
        insert into "Easy"."EscalaTrabalho" ("Escala", "des_periodo1", "periodo1_inicio", "periodo1_fim",
        "des_periodo2", "periodo2_inicio", "periodo2_fim",
        "des_periodo3", "periodo3_inicio", "periodo3_fim"
        ) values ( %s, %s , %s, %s, %s , %s, %s, %s , %s, %s )
        """
        conn = ConexaoPostgreMPL.conexaoJohn()
        cur = conn.cursor()
        cur.execute(insert, (nomeEscala,descricaoPeriodo1 , inicio_periodo1, termino_periodo1,
                         descricaoPeriodo2 , inicio_periodo2, termino_periodo2,
                         descricaoPeriodo3 , inicio_periodo3, termino_periodo3))
        conn.commit()
        cur.close()
        conn.close()
        return pd.DataFrame([{'Mensagem': "ESCALA cadastrada com Sucesso!", "status": True}])

def AtualizarEscalaTrabalho(nomeEscalaAtual,nomeEscalaNova, descricaoPeriodo1 , inicio_periodo1, termino_periodo1,
                          descricaoPeriodo2 , inicio_periodo2, termino_periodo2,
                          descricaoPeriodo3 , inicio_periodo3, termino_periodo3):

    # Verifica se a escala existe
    verfica = ConsultaEscalaTrabalho()
    verfica = verfica[verfica["Escala"] == nomeEscalaAtual].reset_index()

    if verfica.empty:
        return pd.DataFrame([{'Mensagem': "Escala de Trabalho nao existe", "status": False}])
    else:
        if nomeEscalaNova =="-":
            nomeEscalaNova = verfica["Escala"][0]
        if descricaoPeriodo1 =="-":
            descricaoPeriodo1 = verfica["descricaoPeriodo1"][0]
        if descricaoPeriodo2 =="-":
            descricaoPeriodo2 = verfica["descricaoPeriodo2"][0]
        if descricaoPeriodo3 =="-":
            descricaoPeriodo3 = verfica["descricaoPeriodo3"][0]
        if inicio_periodo1 =="-":
            inicio_periodo1 = verfica["inicio_periodo1"][0]
        if inicio_periodo2 =="-":
            inicio_periodo2 = verfica["inicio_periodo2"][0]
        if inicio_periodo3 =="-":
            inicio_periodo3 = verfica["inicio_periodo3"][0]
        if termino_periodo1 =="-":
            termino_periodo1 = verfica["termino_periodo1"][0]
        if termino_periodo2 =="-":
            termino_periodo2 = verfica["termino_periodo2"][0]
        if termino_periodo3 =="-":
            termino_periodo3 = verfica["termino_periodo3"][0]

        update = """
        update "Easy"."EscalaTrabalho"
        set "Escala" = %s , "des_periodo1" = %s , "periodo1_inicio" = %s , "periodo1_fim" = %s ,
        "des_periodo2" = %s , "periodo2_inicio" = %s , "periodo2_fim" = %s ,
        "des_periodo3" = %s , "periodo3_inicio" = %s , "periodo3_fim" = %s 
        where "Escala" = %s
        """

        conn = ConexaoPostgreMPL.conexaoJohn()
        cur = conn.cursor()
        cur.execute(update, (nomeEscalaNova,descricaoPeriodo1 , inicio_periodo1, termino_periodo1,
                         descricaoPeriodo2 , inicio_periodo2, termino_periodo2,
                         descricaoPeriodo3 , inicio_periodo3, termino_periodo3, nomeEscalaAtual))
        conn.commit()
        cur.close()
        conn.close()
        return pd.DataFrame([{'Mensagem': "ESCALA alterada com Sucesso!", "status": True}])