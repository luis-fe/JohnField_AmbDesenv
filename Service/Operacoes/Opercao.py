import pandas as pd
import ConexaoPostgreMPL
from Service import FaseJohnField, CategiaJohnField

def Buscar_Operacoes():
    print('meu teste')
    conn = ConexaoPostgreMPL.conexaoJohn()

    sql = """
        select  c.*, f."nomeFase",c2."nomeCategoria"  ,to2."tempoPadrao" as "TempoPadrao(s)", f."nomeFase", "Maq/Equipamento"  from "Easy"."Operacao" c
    inner join "Easy"."Fase" f on f."codFase" = c."codFase"
    inner join "Easy"."TemposOperacao" to2 on to2."codOperacao" = c."codOperacao" 
    inner join "Easy"."Categoria" c2 on c2.codcategoria = to2."codCategoria" 
    """

    consulta = pd.read_sql(sql,conn)
    conn.close()

    consulta['Pcs/Hora'] = (60*60)/consulta['TempoPadrao(s)']
    consulta['Pcs/Hora'] = consulta['Pcs/Hora'].astype(int)
    print(consulta)

    return consulta

def BuscarOperacaoEspecifica(nomeOperacao, nomeCategoria):
    conn = ConexaoPostgreMPL.conexaoJohn()

    consulta = """
    select * from "Easy"."Operacao" o
    inner join "Easy"."TemposOperacao" to2 on to2."codOperacao" =o."codOperacao" 
    inner join "Easy"."Categoria" c on c.codcategoria = to2 ."codCategoria"
    where o."nomeOperacao" = %s and c."nomeCategoria" = %s
    """

    consulta = pd.read_sql(consulta,conn,params=(nomeOperacao,nomeCategoria,))
    conn.close()

    return consulta

def InserirOperacao(nomeOperacao, nomeFase, Maq_Equipamento, nomeCategoria, tempoPadrao):
    # Passo 1 : Verificar se a operacao atual existe
    consulta = BuscarOperacaoEspecifica(nomeOperacao, nomeCategoria)
    if not consulta.empty:
        return pd.DataFrame([{'Mensagem': "Operacão já´existe!", "status": False}])
    else:
        # Passo 2: Verificando se a Fase informada existe
        codFase = FaseJohnField.BuscarFases()
        codFase = codFase[codFase['nomeFase'] == nomeFase].reset_index()
        if codFase.empty:
            return pd.DataFrame([{'Mensagem': "A Fase informada nao existe!", "status": False}])
        else:
            # Passo 2.1 - Obtendo o codigo da fase
            codFase = codFase['codFase'][0]

            # Passo 3 - Verificando se a categoria informada existe
            consultaCategoria = CategiaJohnField.BuscarCategorias()
            codCategoria = consultaCategoria[consultaCategoria['nomeCategoria']==nomeCategoria].reset_index()

            if codCategoria.empty:
                return pd.DataFrame([{'Mensagem': "A Categoria informada nao existe!", "status": False}])
            else:
                # Passo 3.1 - Obtendo o codigo da categoria
                codCategoria = codCategoria['codcategoria'][0]

                # Passo 4 - Insercao dos dados no banco
                conn = ConexaoPostgreMPL.conexaoJohn()
                inserir = """
                insert into "Easy"."Operacao" ("codFase", "Maq/Equipamento","nomeOperacao") values (%s,  %s, %s )
                """
                cursor = conn.cursor()
                cursor.execute(inserir,(int(codFase) ,Maq_Equipamento,nomeOperacao,))
                conn.commit()

                # Passo 4.1 - Insercao dos dados no banco - TempoPadrao e Categoria
                    # 4.2 - Obtendo o ultimo codOperacao cadastrado
                ultimaOperacao = """
                    select max("codOperacao") as "codOperacao" from "Easy"."Operacao" o
                    """
                ultimaOperacao = pd.read_sql(ultimaOperacao, conn)
                ultimaOperacao = ultimaOperacao['codOperacao'][0]+1


                inserirTempoPadrao = """
                insert into "Easy"."TemposOperacao" ("codOperacao", "codCategoria", "tempoPadrao") values (%s, %s, %s )
                """
                cursor = conn.cursor()
                cursor.execute(inserirTempoPadrao,(int(ultimaOperacao) ,int(codCategoria),float(tempoPadrao)))
                conn.commit()
                conn.close()

                return pd.DataFrame([{'Mensagem': "Operacão cadastrada com Sucesso!", "status": True}])



def UpdateOperacao(codOperacao, nomeOperacao, nomeFase, Maq_Equipamento, nomeCategoria, tempoPadrao):

    # Passo 1 : Verificar se a operacao atual existe
    consulta = Buscar_Operacoes()
    consulta = consulta[consulta['codOperacao'] == codOperacao].reset_index()
    if  consulta.empty:
        return pd.DataFrame([{'Mensagem': "Operacão nao existe!", "status": False}])
    else:


        if nomeFase =='-':
                nomeFase = consulta['nomeFase'][0]
        if Maq_Equipamento =='-':
                Maq_Equipamento = consulta['Maq/Equipamento'][0]
        if nomeCategoria =='-':
                nomeCategoria = consulta['nomeCategoria'][0]
        if tempoPadrao =='-':
                nomeFase = consulta['TempoPadrao(s)'][0]
        if nomeOperacao =='-':
                nomeOperacao = consulta['nomeOperacao'][0]

        consultaCategoria = CategiaJohnField.BuscarCategorias()
        codCategoria = consultaCategoria[consultaCategoria['nomeCategoria'] == nomeCategoria].reset_index()
        if codCategoria.empty:
            return pd.DataFrame([{'Mensagem': "A Categoria informada nao existe!", "status": False}])
        else:
            codCategoria = codCategoria['codcategoria'][0]

            # Passo 2: Verificando se a Fase informada existe
            codFase = FaseJohnField.BuscarFases()
            codFase = codFase[codFase['nomeFase'] == nomeFase].reset_index()
            if codFase.empty:
                return pd.DataFrame([{'Mensagem': "A Fase informada nao existe!", "status": False}])
            else:
                # Passo 2.1 - Obtendo o codigo da fase
                codFase = codFase['codFase'][0]

                conn = ConexaoPostgreMPL.conexaoJohn()
                cur = conn.cursor()


                update = """
                update "Easy"."TemposOperacao" 
                set "codCategoria" = %s ,"tempoPadrao" = %s
                where "codOperacao" = %s
                """
                cur.execute(update,(int(codCategoria),float(tempoPadrao),codOperacao))
                conn.commit()

                update2 = """
                update "Easy"."Operacao" 
                set "codFase" = %s, "Maq/Equipamento" =%s, "nomeOperacao" = %s
                where "codOperacao" = %s
                """
                cur.execute(update2,(int(codFase),Maq_Equipamento,nomeOperacao,codOperacao))
                conn.commit()

                cur.close()
                conn.close()
                return pd.DataFrame([{'Mensagem': "Operacão Alterado com sucesso!", "status": True}])
