import pandas as pd
import ConexaoPostgreMPL


def OPsAbertoPorCliente(nomeCliente = ''):

    consulta = """
    select * from "Easy"."DetalhaOP_Abertas" doa 
    order by "codFase" asc 
    """

    quantidade = """
      select "idOP" , sum(quantidade) as quantidade  from "Easy"."OP_Cores_Tam" oct 
  group by oct."idOP" 
    """

    conn = ConexaoPostgreMPL.conexaoJohn()
    consulta = pd.read_sql(consulta,conn)
    quantidade = pd.read_sql(quantidade,conn)
    consulta['idOP'] = consulta["codOP"] +'||'+consulta["codCliente"].astype(str)

    conn.close()


    consulta = pd.merge(consulta,quantidade,on='idOP',how='left')
    consulta['quantidade'].fillna(0, inplace=True)
    consulta = consulta

    pcsAberto1 = consulta['quantidade'].sum()
    pcsAberto = round(pcsAberto1)
    pcsAberto = '{:,.0f}'.format(pcsAberto)
    pcsAberto = pcsAberto.replace(',', '.')

    OPAberto = consulta['codOP'].count()
    OPAberto = round(OPAberto)
    OPAberto = '{:,.0f}'.format(OPAberto)
    OPAberto = OPAberto.replace(',', '.')

    ClienteAberto = consulta['codCliente'].drop_duplicates().count()
    ClienteAberto = round(ClienteAberto)
    ClienteAberto = '{:,.0f}'.format(ClienteAberto)
    ClienteAberto = ClienteAberto.replace(',', '.')


    consulta['dataCriacaoOP'] = pd.to_datetime(consulta['dataCriacaoOP'], format='%a, %d %b %Y %H:%M:%S %Z')
    consulta['dataCriacaoOP'] = consulta['dataCriacaoOP'].dt.strftime('%d/%m/%Y')

    consulta['situacaoLeadTime'] = consulta.apply(lambda r : 'Atrasado'if r['LeadTimeMeta'] < r['diasEmAberto'] else 'No Prazo', axis=1 )

    DistribuicaoClientes = consulta.groupby(['codCliente', 'nomeCliente']).agg(
        quantidadeOP=('codCliente', 'size'),quantidadePc=('quantidade', 'sum')).reset_index()
    print(DistribuicaoClientes)

    DistribuicaoClientes['quantidadeOP%'] = round((DistribuicaoClientes['quantidadeOP']/int(OPAberto))*100)
    DistribuicaoClientes['quantidadePc%'] = round((DistribuicaoClientes['quantidadePc']/float(pcsAberto1))*100)


    if nomeCliente != '':
        consulta = consulta[consulta['nomeCliente'] == nomeCliente]
        OPAberto = consulta['codOP'].count()
        OPAberto = round(OPAberto)
        OPAberto = '{:,.0f}'.format(OPAberto)
        OPAberto = OPAberto.replace(',', '.')

        pcsAberto = consulta['quantidade'].sum()
        pcsAberto = round(pcsAberto)
        pcsAberto = '{:,.0f}'.format(pcsAberto)
        pcsAberto = pcsAberto.replace(',', '.')

    dados = {
        '0-Total De pçs em Aberto': f'{pcsAberto} Pçs ',
        '1- Total De OPs em Abero': f'{OPAberto} OPs ',
        '2- Total de Clientes em Aberto':f'{ClienteAberto} Clientes ',
        '3- DistribuicaoClientes':DistribuicaoClientes.to_dict(orient='records'),
        '4 -DetalhamentoEmAberto': consulta.to_dict(orient='records')}

    return pd.DataFrame([dados])


def OpsAbertoPorFase(nomeFase = ''):
    consulta = """
select * from "Easy"."DetalhaOP_Abertas" doa 
order by "codFase"      
"""

    quantidade = """
        select "idOP" , sum(quantidade) as quantidade  from "Easy"."OP_Cores_Tam" oct 
    group by oct."idOP" 
      """

    conn = ConexaoPostgreMPL.conexaoJohn()
    consulta = pd.read_sql(consulta, conn)
    quantidade = pd.read_sql(quantidade, conn)
    consulta['idOP'] = consulta["codOP"] + '||' + consulta["codCliente"].astype(str)

    conn.close()

    consulta = pd.merge(consulta, quantidade, on='idOP', how='left')
    consulta['quantidade'].fillna(0, inplace=True)
    consulta = consulta

    pcsAberto1 = consulta['quantidade'].sum()
    pcsAberto = round(pcsAberto1)
    pcsAberto = '{:,.0f}'.format(pcsAberto)
    pcsAberto = pcsAberto.replace(',', '.')

    OPAberto = consulta['codOP'].count()
    OPAberto = round(OPAberto)
    OPAberto = '{:,.0f}'.format(OPAberto)
    OPAberto = OPAberto.replace(',', '.')

    FasesAberto = consulta['FaseAtual'].drop_duplicates().count()
    FasesAberto = round(FasesAberto)
    FasesAberto = '{:,.0f}'.format(FasesAberto)
    FasesAberto = FasesAberto.replace(',', '.')





    consulta['dataCriacaoOP'] = pd.to_datetime(consulta['dataCriacaoOP'], format='%a, %d %b %Y %H:%M:%S %Z')
    consulta['dataCriacaoOP'] = consulta['dataCriacaoOP'].dt.strftime('%d/%m/%Y')

    consulta['situacaoLeadTime'] = consulta.apply(lambda r : 'Atrasado'if r['LeadTimeMeta'] < r['diasEmAberto'] else 'No Prazo', axis=1 )

    atrasados = consulta[consulta['situacaoLeadTime'] == 'Atrasado']

    # Agregação para contar OPs atrasadas por fase
    DistribuicaoAtrasados = atrasados.groupby(['FaseAtual']).agg(
        qtdOPAtrasada=('codCliente', 'size')
    ).reset_index()


    DistribuicaoClientes = consulta.groupby(['FaseAtual']).agg(
        quantidadeOP=('codCliente', 'size'),
        quantidadePc=('quantidade', 'sum'),
        codFase=('codFase','first')
    ).reset_index()
    DistribuicaoClientes = DistribuicaoClientes.sort_values(by=['codFase'], ascending=True)  # escolher como deseja classificar

    DistribuicaoClientes['quantidadeOP%'] = round((DistribuicaoClientes['quantidadeOP'] / int(OPAberto)) * 100)
    DistribuicaoClientes['quantidadePc%'] = round((DistribuicaoClientes['quantidadePc'] / float(pcsAberto1)) * 100)

    DistribuicaoClientes = DistribuicaoClientes.merge(DistribuicaoAtrasados, on='FaseAtual', how='left')
    DistribuicaoClientes['qtdOPAtrasada'] = DistribuicaoClientes['qtdOPAtrasada'].fillna(0)


    OPAbertoAtr = atrasados['codOP'].count()
    OPAbertoAtr = round(OPAbertoAtr)
    OPAbertoAtr = '{:,.0f}'.format(OPAbertoAtr)
    OPAbertoAtr = OPAbertoAtr.replace(',', '.')

    if nomeFase !='':
        consulta = consulta[consulta['FaseAtual']==nomeFase]
        OPAberto = consulta['codOP'].count()
        OPAberto = round(OPAberto)
        OPAberto = '{:,.0f}'.format(OPAberto)
        OPAberto = OPAberto.replace(',', '.')

        pcsAberto = consulta['quantidade'].sum()
        pcsAberto = round(pcsAberto)
        pcsAberto = '{:,.0f}'.format(pcsAberto)
        pcsAberto = pcsAberto.replace(',', '.')

        OPAbertoAtr = atrasados['codOP'].count()
        OPAbertoAtr = round(OPAbertoAtr)
        OPAbertoAtr = '{:,.0f}'.format(OPAbertoAtr)
        OPAbertoAtr = OPAbertoAtr.replace(',', '.')




    dados = {
        '0-Total De pçs em Aberto': f'{pcsAberto} Pçs ',
        '1- Total De OPs em Abero': f'{OPAberto} OPs ',
        '2- Total de Fases em Aberto': f'{FasesAberto} Fases ',
        '2.1- Total de OPs em Atraso': f'{OPAbertoAtr} OPs ',
        '3- DistribuicaoFases': DistribuicaoClientes.to_dict(orient='records'),
        '4 -DetalhamentoEmAberto': consulta.to_dict(orient='records')}

    return pd.DataFrame([dados])



def RankingOperadoresEficiencia(dataInico, dataFinal):

    sql = """
    select
    "Codigo Registro",
	"Data" ,
	"Hr Inicio" ,"Hr Final" ,
	"codOperador" ,
	"nomeOperador",
	"paradas min",
	"tempoTotal(min)",
	"qtdPcs", "Meta(pcs/hr)" 
    from
	"Easy"."ColetasProducao" cp
    where "Data" >= %s and "Data" <= %s
    order by "Data" ,  "codOperador", "Codigo Registro"
    """


    conn = ConexaoPostgreMPL.conexaoJohn()
    produtividade =pd.read_sql(sql,conn,params=(dataInico, dataFinal))

    if produtividade.empty:
        return pd.DataFrame([])
    else:
        produtividade['tempoTotal(min)Acum'] = produtividade.groupby(['Data','codOperador'])['tempoTotal(min)'].cumsum()
        produtividade['tempo Previsto'] = round(produtividade['Meta(pcs/hr)']/60,2) * produtividade['qtdPcs']
        produtividade['tempo PrevistoAcum'] = produtividade.groupby(['Data','codOperador'])['tempo Previsto'].cumsum()
        produtividade['tempo PrevistoAcum'] = produtividade['tempo PrevistoAcum'].round(2)
        produtividade['qtdPcsAcum'] = produtividade.groupby(['Data','codOperador'])['qtdPcs'].cumsum()

        consulta = produtividade.groupby(['Data','codOperador']).agg({
            "Codigo Registro": 'max'}).reset_index()

        consulta = pd.merge(consulta,produtividade,on=['Data','codOperador','Codigo Registro'])
        consulta['Eficiencia'] = round(consulta['tempoTotal(min)Acum']/consulta['tempo PrevistoAcum'],3)*100
        consulta['Eficiencia'] = consulta['Eficiencia'].round(1)

        consulta2 = consulta.groupby('codOperador').agg({
        'nomeOperador':'first',
        'qtdPcsAcum':'sum',
        'tempo PrevistoAcum':'sum',
        'tempoTotal(min)Acum':'sum'
        }).reset_index()
        consulta2['tempoTotal(min)Acum'] = consulta2['tempoTotal(min)Acum'].round(4)
        consulta2['Eficiencia'] = round(consulta2['tempoTotal(min)Acum']/consulta2['tempo PrevistoAcum'],3)*100
        consulta2['Eficiencia'] = consulta2['Eficiencia'].round(1)

        consulta2 = consulta2.sort_values(by=['Eficiencia'], ascending=False)
        consulta2['Eficiencia'] = consulta2['Eficiencia'].astype(str)+'%'

        efiMedia = round(consulta2['tempoTotal(min)Acum'].sum() /consulta2['tempo PrevistoAcum'].sum(),3)*100

        dados = {
            '0-Eficiencia Média Periodo': f'{efiMedia}%',
            '1-Detalhamento': consulta2.to_dict(orient='records')}

        return pd.DataFrame([dados])


def RankingOperacoesEficiencia(dataInico, dataFinal):

    sql = """
    select
    "Codigo Registro",
	"Data" ,
	"Hr Inicio" ,"Hr Final" ,
	"codOperador" ,
	"nomeOperador","nomeOperacao" ,
	"paradas min",
	"tempoTotal(min)",
	"qtdPcs", "Meta(pcs/hr)" 
    from
	"Easy"."ColetasProducao" cp
    where "Data" >= %s and "Data" <= %s
    order by "Data" ,  "codOperador", "Codigo Registro"
    """


    conn = ConexaoPostgreMPL.conexaoJohn()
    produtividade =pd.read_sql(sql,conn,params=(dataInico, dataFinal))

    if produtividade.empty:
        return pd.DataFrame([])
    else:
        produtividade['tempoTotal(min)Acum'] = produtividade.groupby(['Data','nomeOperacao'])['tempoTotal(min)'].cumsum()
        produtividade['tempo Previsto'] = round(produtividade['Meta(pcs/hr)']/60,2) * produtividade['qtdPcs']
        produtividade['tempo PrevistoAcum'] = produtividade.groupby(['Data','nomeOperacao'])['tempo Previsto'].cumsum()
        produtividade['tempo PrevistoAcum'] = produtividade['tempo PrevistoAcum'].round(2)
        produtividade['qtdPcsAcum'] = produtividade.groupby(['Data','nomeOperacao'])['qtdPcs'].cumsum()

        consulta = produtividade.groupby(['Data','nomeOperacao','codOperador']).agg({
            "Codigo Registro": 'max'}).reset_index()

        consulta = pd.merge(consulta,produtividade,on=['Data','codOperador','Codigo Registro','nomeOperacao'])
        consulta['Eficiencia'] = round(consulta['tempoTotal(min)Acum']/consulta['tempo PrevistoAcum'],3)*100
        consulta['Eficiencia'] = consulta['Eficiencia'].round(1)

        consulta2 = consulta.groupby('nomeOperacao').agg({
        'qtdPcsAcum':'sum',
        'tempo PrevistoAcum':'sum',
        'tempoTotal(min)Acum':'sum'
        }).reset_index()
        consulta2['tempoTotal(min)Acum'] = consulta2['tempoTotal(min)Acum'].round(4)
        consulta2['Eficiencia'] = round(consulta2['tempoTotal(min)Acum']/consulta2['tempo PrevistoAcum'],3)*100
        consulta2['Eficiencia'] = consulta2['Eficiencia'].round(1)

        consulta2 = consulta2.sort_values(by=['Eficiencia'], ascending=False)
        consulta2['Eficiencia'] = consulta2['Eficiencia'].astype(str)+'%'

        efiMedia = round(consulta2['tempoTotal(min)Acum'].sum() /consulta2['tempo PrevistoAcum'].sum(),3)*100

        dados = {
            '0-Eficiencia Média Periodo': f'{efiMedia}%',
            '1-Detalhamento': consulta2.to_dict(orient='records')}

        return pd.DataFrame([dados])