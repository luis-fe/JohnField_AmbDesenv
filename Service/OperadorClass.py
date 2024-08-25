import ConexaoPostgreMPL
import pandas as pd


class Operador():
    '''classe Operador : Operador são funcionarios que trabalham diretamente na produção '''
    def __init__(self, codOperador = None, nomeOperador = None):
        '''
        Construtor da Classe com os atributos
        :arg
        :param codOperador:
        :param nomeOperador:
        '''
        self.codOperador = codOperador
        self.nomeOperador = nomeOperador

    def buscarNomeOperador(self):
        conn = ConexaoPostgreMPL.conexaoEngine()
        consulta = """  
                    select
                        "codOperador",
                        "nomeOperador"
                    from
                        "Easy"."Operador"
                    where "codOperador"::varchar = %s
        """

        consulta = pd.read_sql(consulta,conn,params=(str(self.codOperador),))

        return consulta['nomeOperador'][0]
