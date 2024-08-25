import ConexaoPostgreMPL
import pandas as pd
import re
from Service import OperadorClass

class Paradas():
    def __init__(self, dataInicio, dataFinal, horaInicio = None, horaFinal = None, codOperador = None, motivo = '-'):
        self.dataInicio = dataInicio
        self.dataFinal = dataFinal
        self.horaInicio = horaInicio
        self.horaFinal= horaFinal
        self.codOperador= codOperador

        if self.codOperador != None:
            operadorObjeto = OperadorClass.Operador(self.codOperador)
            self.nomeOperador = operadorObjeto.buscarNomeOperador()
        else:
            self.nomeOperador = None

        self.motivo= motivo

    def InserirParada(self):

        validacao = self.ValidarEnvioDataHorario()

        if validacao['Status'][0] == False:
            return validacao
        else:
            insert = """INSERT INTO "Easy"."ApontaParadas"  ("dataInicio", "dataFinal", "horaInicio", 
            "horaFinal", "codOperador", "nomeOperador", "motivo" ) values (%s, %s, %s,%s,%s,%s,%s )"""

            with ConexaoPostgreMPL.conexaoJohn() as conn:
                with conn.cursor() as curr:
                    curr.execute(insert,(self.dataInicio, self.dataFinal, 
                                         self.horaInicio, self.horaFinal, 
                                         self.codOperador, self.nomeOperador, self.motivo))
                    conn.commit()

            return pd.DataFrame([{'Status':True, 'Mensagem':'Inserido com sucesso!'}])


    def UpdateParada(self, dataInicioNovo, dataFinalNovo, horaInicioNovo, horaFinaNovo ):

        validacao = self.ValidarEnvioDataHorario()

        if validacao['Status'][0] == False:
            return validacao
        else:
            update = """UPDATE Easy"."ApontaParadas" SET "dataInicio" = %s , "dataFinal"= %s, "horaInicio"= %s, 
        "horaFinal"= %s, "codOperador"= %s, "nomeOperador"= %s, "motivo"= %s 
        where "dataInicio" = %s
         and "horaInicio"= %s  and "codOperador"= %s"""

            with ConexaoPostgreMPL.conexaoJohn() as conn:
                with conn.cursor() as curr:
                    curr.execute(update,(self.dataInicio, self.dataFinal, self.horaInicio, self.horaFinal, self.codOperador, self.nomeOperador, self.motivo, dataInicioNovo
                                        , dataFinalNovo, horaInicioNovo, horaFinaNovo))
                    conn.commit()



            return pd.DataFrame([{'Status':True, 'Mensagem':'Alterado com sucesso!'}])


    def ExcluirParada(self):

        delete = """DELETE FROM Easy"."ApontaParadas" where "dataInicio" = %s
         and "horaInicio"= %s and "codOperador"= %s"""
        with ConexaoPostgreMPL.conexaoJohn() as conn:
            with conn.cursor() as curr:
                curr.excute(delete,(self.dataInicio,self.horaInicio, self.codOperador))

        return pd.DataFrame([{'Status': True, 'Mensagem': 'Apontamento excluido com sucesso!'}])

    def ConsultarParadasPerido(self):
        conn = ConexaoPostgreMPL.conexaoEngine()
        consulta ="""
                    select
                        *
                    from"Easy"."ApontaParadas" ap where "dataInicio"::Date >= %s and "dataFinal":date <= %s """
        consulta = pd.read_sql(consulta,conn,params=(self.dataInicio, self.dataFinal))
        return consulta

    def ValidarEnvioDataHorario(self):
        # Expressão regular para verificar o formato hh:mm
        padrao_horario = r'^\d{2}:\d{2}$'

        if re.match(padrao_horario, self.horaInicio):
            situacao1 = True
        else:
            situacao1 = False

        if re.match(padrao_horario, self.horaFinal):
            situacao2 = True
        else:
            situacao2 = False

        if situacao1 == False and situacao2 == False:
            return pd.DataFrame([{'Status':False,"Mensagem":'horario nao esta no formato hh:mm '}])
        else:
            return pd.DataFrame([{'Status':True,"Mensagem":'horario  esta no formato hh:mm '}])