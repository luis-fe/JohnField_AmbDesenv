import ConexaoPostgreMPL
import pandas as pd

class Operacao():
    def __init__(self,nomeOperacao=None, codFase=None,
                  MaqEquipamento=None, categoriaOperacao=None,tempoOperacao=None,codOperacao =None):
        self.codOperacao = codOperacao
        self.nomeOperacao = nomeOperacao
        self.codFase = codFase
        self.MaqEquipamento = MaqEquipamento
        self.categoriaOperacao = categoriaOperacao 
        self.tempoOperacao = tempoOperacao 

    def ObterUltimaOperacao(self):
        conn = ConexaoPostgreMPL.conexaoJohn()
        #Obtendo o ultimo codOperacao cadastrado
        sqlultimaOperacao = """
                    select max("codOperacao") as "codOperacao" from "Easy"."Operacao" o
                    """
        cursor = conn.cursor()
        cursor.execute(sqlultimaOperacao)
        ultimaOperacao = cursor.fetchone()
        ultimaOperacao = ultimaOperacao[0]
        return ultimaOperacao

    
    def InserirOperacao(self):
        conn = ConexaoPostgreMPL.conexaoJohn()
        insert = """
                insert into "Easy"."Operacao" ("codFase", "Maq/Equipamento","nomeOperacao",categoriaoperacao)
                  values (%s,  %s, %s, %s )
        """
        inserirTempoPadrao = """
                insert into "Easy"."TemposOperacao" ("codOperacao", "tempoPadrao") 
                values (%s, %s )
        """
        #Obtendo o ultimo codOperacao cadastrado
        sqlultimaOperacao = """
                    select max("codOperacao") as "codOperacao" from "Easy"."Operacao" o
                    """
        
        cursor = conn.cursor()
        
        cursor.execute(insert,(self.codFase,self.MaqEquipamento,self.nomeOperacao, self.categoriaOperacao))
        conn.commit()


        self.codOperacao = self.ObterUltimaOperacao()

        
        cursor.execute(inserirTempoPadrao,(ultimaOperacao,self.tempoOperacao))
        conn.commit()

        cursor.close()
        conn.close()
        return pd.DataFrame([{'Mensagem': "Operacão cadastrada com Sucesso!", "status": True}])
    
    def BuscarOperacoes(self):
        conn = ConexaoPostgreMPL.conexaoEngine()

        sql = """
            select  c.*, f."nomeFase",c2."nomeCategoria"  ,to2."tempoPadrao" as "TempoPadrao(s)", f."nomeFase", "Maq/Equipamento"  from "Easy"."Operacao" c
        inner join "Easy"."Fase" f on f."codFase" = c."codFase"
        inner join "Easy"."TemposOperacao" to2 on to2."codOperacao" = c."codOperacao" 
        inner join "Easy"."Categoria" c2 on c2.codcategoria = to2."codCategoria" 
        """
        consulta = pd.read_sql(sql,conn)
        consulta['Pcs/Hora'] = (60*60)/consulta['TempoPadrao(s)']
        consulta['Pcs/Hora'] = consulta['Pcs/Hora'].astype(int)

        return consulta
    
    def BuscarOperacaoEspecifica(self):
        conn = ConexaoPostgreMPL.conexaoEngine()

        consulta = """
    select * from "Easy"."Operacao" o
    inner join "Easy"."TemposOperacao" to2 on to2."codOperacao" =o."codOperacao" 
    where o."nomeOperacao" = %s
    """
        consulta = pd.read_sql(consulta,conn,params=(self.nomeOperacao,))
        consulta.rename(
        columns={'categoriaoperacao': 'CategoriaOperacao'},
        inplace=True)

        return consulta
    
    def UpdateOperacao(self):
        #Validar se existe a operacao
        validar = self.BuscarOperacaoEspecifica()
        if validar.empty:
            return pd.DataFrame([{'Mensagem': "Operacão nao existe!", "status": False}])
        else:
            conn = ConexaoPostgreMPL.conexaoJohn()
            cur = conn.cursor()

            if self.tempoOperacao != None:
                update = """
                    update "Easy"."TemposOperacao" 
                    set "tempoPadrao" = %s
                    where "codOperacao" = %s
                    """
                cur.execute(update,(float(self.tempoOperacao),self.codOperacao))
                conn.commit()
            if self.codFase == None:
                self.codFase=validar['codFase'][0]
            
            if self.MaqEquipamento == None:
                self.MaqEquipamento=validar['Maq/Equipamento'][0]
            
            if self.nomeOperacao == None:
                self.nomeOperacao=validar['nomeOperacao'][0]

            if self.categoriaOperacao == None:
                self.categoriaOperacao=validar['CategoriaOperacao'][0]

            
            update2 = """
                update "Easy"."Operacao" 
                set "codFase" = %s, "Maq/Equipamento" =%s, "nomeOperacao" = %s, categoriaoperacao = %s
                where "codOperacao" = %s
                """
            cur.execute(update2,(self.codFase,self.MaqEquipamento,self.nomeOperacao,
                                 self.categoriaOperacao,self.codOperacao, ))
            conn.commit()

            cur.close()
            conn.close()
            return pd.DataFrame([{'Mensagem': "Operacão Alterado com sucesso!", "status": True}])


    
