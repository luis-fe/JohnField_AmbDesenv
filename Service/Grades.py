import pandas as pd
import ConexaoPostgreMPL


def BuscarGrade():
    consulta = """
    SELECT "codGrade", "nomeGrade", "Tamanhos" FROM "Easy"."Grade"
    """
    conn = ConexaoPostgreMPL.conexaoJohn()
    consulta = pd.read_sql(consulta, conn)
    conn.close()

    # Convertendo a coluna 'Tamanhos' para lista de strings
    consulta['Tamanhos'] = consulta['Tamanhos'].apply(lambda x: [x])

    # Agrupar tamanhos em uma lista
    df_summary = consulta.groupby(['codGrade', 'nomeGrade'])['Tamanhos'].sum().reset_index()

    return df_summary


def BuscarGradeEspecifica(codGrade):
    buscar = BuscarGrade()
    buscar = buscar[buscar['codGrade'] == codGrade]

    return buscar

def NovaGrade(codGrade, nomeGrade, arrayTamanhos):
    VerificarGrade = BuscarGradeEspecifica(codGrade)
    if not VerificarGrade.empty:
        return pd.DataFrame([{'Mensagem': f'Grade {codGrade} já existe!', 'status': False}])
    else:
        conn = ConexaoPostgreMPL.conexaoJohn()

        for tamanho in arrayTamanhos:  # Correção do loop

            inserir = """
            INSERT INTO "Easy"."Grade" ("codGrade", "nomeGrade", "Tamanhos")
            VALUES (%s, %s, %s)  -- Correção na sintaxe do SQL
            """
            cursor = conn.cursor()
            cursor.execute(inserir, (codGrade, nomeGrade, tamanho,))
            conn.commit()

            cursor.close()

        conn.close()
        return pd.DataFrame([{'Mensagem': f'Grade {codGrade} cadastrada com sucesso!', 'status': True}])

def UpdateGrade(codGrade, nomeGrade, arrayTamanhos):
    VerificarGrade = BuscarGradeEspecifica(codGrade)
    if VerificarGrade.empty:
        return pd.DataFrame([{'Mensagem': f'Grade {codGrade} NAO já existe!', 'status': False}])
    else:
        conn = ConexaoPostgreMPL.conexaoJohn()


        delete = """
            delete from "Easy"."Grade"
            where "codGrade" = %s            
            """

        cursor = conn.cursor()

        cursor.execute(delete,(codGrade,))
        conn.commit()
        cursor.close()

        for tamanho in arrayTamanhos:  # Correção do loop

                inserir = """
                INSERT INTO "Easy"."Grade" ("codGrade", "nomeGrade", "Tamanhos")
                VALUES (%s, %s, %s)  -- Correção na sintaxe do SQL
                """
                cursor = conn.cursor()
                cursor.execute(inserir, (codGrade, nomeGrade, tamanho,))
                conn.commit()

                cursor.close()


        conn.close()
        return pd.DataFrame([{'Mensagem': f'Grade {codGrade} Atualizada com sucesso!', 'status': True}])

def ObterTamanhos():
    conn = ConexaoPostgreMPL.conexaoJohn()

    consulta = """
    select codsequencia , "DescricaoTamanho"  from "Easy"."Tamanhos" t 
order by t.codsequencia asc
    """
    consulta = pd.read_sql(consulta,conn)
    conn.close()

    return consulta

def ObterTamanhoEspecifico(DescricaoTamanho):
    consulta = ObterTamanhos()
    consulta = consulta[consulta['DescricaoTamanho'] == DescricaoTamanho]
    return consulta

def ObterSequencia(codsequencia):
    consulta = ObterTamanhos()
    consulta = consulta[consulta['codsequencia'] == codsequencia]
    return consulta

def InserirTamanho(sequenciaTamanho, DescricaoTamanho):
    VerificarTamanho = ObterTamanhoEspecifico(DescricaoTamanho)
    VerificarSequencia = ObterSequencia(sequenciaTamanho)
    VerificarSequenciaContagem = ObterTamanhos()
    VerificarSequenciaContagem = VerificarSequenciaContagem['codsequencia'].count()

    if sequenciaTamanho == '':
        sequenciaTamanho = 0

    if sequenciaTamanho == 0 or sequenciaTamanho > int(VerificarSequenciaContagem + 1)  :
        sequenciaTamanho = int(VerificarSequenciaContagem + 1)
        print(sequenciaTamanho)

    if VerificarTamanho.empty and VerificarSequencia.empty:

        inserir = """
        insert into "Easy"."Tamanhos" (codsequencia , "DescricaoTamanho") values ( %s , %s )
        """
        conn = ConexaoPostgreMPL.conexaoJohn()
        cursor = conn.cursor()

        cursor.execute(inserir,(sequenciaTamanho,DescricaoTamanho,))
        conn.commit()

        cursor.close()
        conn.close()

        return pd.DataFrame([{'Mensagem':'Tamanho Inserido com Sucesso!','status':True}])

    elif not VerificarTamanho.empty :

        return pd.DataFrame([{'Mensagem':'Tamanho já EXISTE!','status':False}])

    else:

        updateSequencias = """
        update "Easy"."Tamanhos"
        set codsequencia = codsequencia + 1
        where codsequencia => %s
        """

        inserir = """
        insert into "Easy"."Tamanhos" (codsequencia , "DescricaoTamanho") values ( %s , %s )
        """
        conn = ConexaoPostgreMPL.conexaoJohn()
        cursor = conn.cursor()

        cursor.execute(updateSequencias,(sequenciaTamanho,))
        conn.commit()

        cursor.execute(inserir,(sequenciaTamanho,DescricaoTamanho,))
        conn.commit()

        cursor.close()
        conn.close()

        return pd.DataFrame([{'Mensagem':'Tamanho Inserido com Sucesso!','status':True, 'Mensagem2':'Sequencia de Tamanhos Reordenados!'}])


def UpdateDescricaoTamanho(codsequencia, DescricaoTamanho):
    VerificarSequencia= ObterSequencia(codsequencia)
    VerificarTamanho = ObterTamanhoEspecifico(DescricaoTamanho)


    if VerificarSequencia.empty :

        return pd.DataFrame([{'Mensagem':f'Sequencia {codsequencia} nao exite!','status':False}])
    elif not VerificarTamanho.empty :

        return pd.DataFrame([{'Mensagem':f'Tamanho {DescricaoTamanho} ja exite!','status':False}])

    # Caso apenas a Descricao tamanho tenha sido alterado:
    #---------------------------------------------------------------------
    else:

        update = """
            update "Easy"."Tamanhos"
            set "DescricaoTamanho" = %s
            where "codsequencia" = %s
        """
        conn = ConexaoPostgreMPL.conexaoJohn()
        cursor = conn.cursor()

        cursor.execute(update, (DescricaoTamanho, codsequencia,))
        conn.commit()
        cursor.close()
        conn.close()

        return pd.DataFrame([{'Mensagem': 'Tamanho Alterado com sucesso', 'Status': True}])