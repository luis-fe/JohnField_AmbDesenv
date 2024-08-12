import pandas as pd
import ConexaoPostgreMPL



def ConsultarCategoriaOperacao():

    sql = """
    select c.id_categoria, c.nomecategoria as "CategoriaOperacao" , c.metadiaria as "MetaDiaria" from "Easy".categoriaoperacao c 
    """

    conn = ConexaoPostgreMPL.conexaoEngine()
    consulta = pd.read_sql(sql,conn)

    return consulta


def InserirCategoria(CategoriaOperacao, MetaDiaria):

    #Verificar
    verificar = ConsultarCategoriaOperacao()
    verificar1 = verificar[verificar['CategoriaOperacao']==CategoriaOperacao].reset_index()

    if not verificar1.empty:
        return pd.DataFrame([{'Status': False, "Mensagem":"Categora Ja utiizada" }])
    else:
        ultimoPonto = verificar['id_categoria'].max() + 1
        insert = """INSERT INTO "Easy".categoriaoperacao (id_categoria, nomecategoria, metadiaria) VALUES ( %s ,%s ,%s ) """

        conn = ConexaoPostgreMPL.conexaoJohn()
        with conn.cursor() as curr:
            curr.execute(insert,(int(ultimoPonto),CategoriaOperacao, int(MetaDiaria)))
            conn.commit()
        conn.close()
        return pd.DataFrame([{'Status': True, "Mensagem":"Categora Salva Com Sucesso !" }])

def AlterarMeta(CategoriaOperacao, MetaDiaria):
    #Verificar
    verificar = ConsultarCategoriaOperacao()
    verificar1 = verificar[verificar['CategoriaOperacao']==CategoriaOperacao].reset_index()

    if  verificar1.empty:
        return pd.DataFrame([{'Status': False, "Mensagem":"Categora Nao exite " }])
    else:
        update ="""update "Easy".categoriaoperacao set metadiaria = %s where nomecategoria = %s """
        conn = ConexaoPostgreMPL.conexaoJohn()
        with conn.cursor() as curr:
            curr.execute(update,(int(MetaDiaria),CategoriaOperacao,))
            conn.commit()
        conn.close()
        return pd.DataFrame([{'Status': True, "Mensagem":"Categora Salva Com Sucesso !" }])



