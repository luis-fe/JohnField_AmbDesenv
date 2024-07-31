from flask import Blueprint, jsonify, request
from functools import wraps
from Service.Operacoes import ColetaProducao
import pandas as pd

ColetaProducao_routesJohn = Blueprint('ColetaProdJohn', __name__) # Esse é o nome atribuido para o conjunto de rotas envolvendo usuario

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token == 'Easy445277888':  # Verifica se o token é igual ao token fixo
            return f(*args, **kwargs)
        return jsonify({'message': 'Acesso negado'}), 401

    return decorated_function



@ColetaProducao_routesJohn.route('/api/JonhField/RegistrarProducao', methods=['POST'])
@token_required
def post_RegistrarProducao():
    data = request.get_json()
    nomeOperacao = data.get('nomeOperacao')
    codOperador = data.get('codOperador')
    nomeCategoria = data.get('nomeCategoria')
    qtdPecas = data.get('qtdPecas','-')

    consulta = ColetaProducao.ColetaProducao(codOperador, nomeOperacao, qtdPecas )
    # Obtém os nomes das colunas
    column_names = consulta.columns
    # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
    consulta_data = []
    for index, row in consulta.iterrows():
        consulta_dict = {}
        for column_name in column_names:
            consulta_dict[column_name] = row[column_name]
        consulta_data.append(consulta_dict)
    return jsonify(consulta_data)


@ColetaProducao_routesJohn.route('/api/JonhField/RegistroRetroativoProducao', methods=['POST'])
@token_required
def post_RegistroRetroativoProducao():
    data = request.get_json()
    nomeOperacao = data.get('nomeOperacao')
    codOperador = data.get('codOperador')
    qtdPecas = data.get('qtdPecas','-')
    dataRetroativa =data.get('dataRetroativa','-')
    HorarioTermino =data.get('HorarioTermino','-')


    consulta = ColetaProducao.ColetaProducaoRetroativa(codOperador, nomeOperacao, qtdPecas,dataRetroativa, HorarioTermino )
    # Obtém os nomes das colunas
    column_names = consulta.columns
    # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
    consulta_data = []
    for index, row in consulta.iterrows():
        consulta_dict = {}
        for column_name in column_names:
            consulta_dict[column_name] = row[column_name]
        consulta_data.append(consulta_dict)
    return jsonify(consulta_data)


@ColetaProducao_routesJohn.route('/api/JonhField/RegistroPorPeriodo', methods=['GET'])
@token_required
def get_RegistroPorPeriodo():

        codOperador = request.args.get('codOperador', '')
        dataInicio = request.args.get('dataInicio', '')
        dataFim = request.args.get('dataFim', '')
        print(dataInicio)

        busca = ColetaProducao.ConsultaRegistroPorPeriodo(codOperador, dataInicio, dataFim)

        # Verifica se 'busca' é um DataFrame
        if not isinstance(busca, pd.DataFrame):
            return jsonify({'error': 'Unexpected data format'}), 500

        # Obtém os nomes das colunas
        column_names = busca.columns.tolist()

        # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
        consulta_data = busca.to_dict(orient='records')

        return jsonify(consulta_data)

@ColetaProducao_routesJohn.route('/api/JonhField/ApontarAusencia', methods=['POST'])
@token_required
def post_ApontarAusencia():
    data = request.get_json()
    codOperador = data.get('codOperador')
    Data = data.get('Data')
    InicioAusencia = data.get('InicioAusencia')
    FimAusencia = data.get('FimAusencia')
    motivo = data.get('motivo')
    aplicaDesconto = data.get('aplicaDesconto')

    consulta = ColetaProducao.ApontamentoParadas(codOperador, Data, InicioAusencia , FimAusencia, motivo,aplicaDesconto)
    # Obtém os nomes das colunas
    column_names = consulta.columns
    # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
    consulta_data = []
    for index, row in consulta.iterrows():
        consulta_dict = {}
        for column_name in column_names:
            consulta_dict[column_name] = row[column_name]
        consulta_data.append(consulta_dict)
    return jsonify(consulta_data)


@ColetaProducao_routesJohn.route('/api/JonhField/ConsultaPardas', methods=['GET'])
@token_required
def get_ConsultaPardas():

        DataInicio = request.args.get('DataInicio', '')
        DataFinal = request.args.get('DataFinal', '')

        busca = ColetaProducao.ConsultaPardas(DataInicio, DataFinal)

        # Verifica se 'busca' é um DataFrame
        if not isinstance(busca, pd.DataFrame):
            return jsonify({'error': 'Unexpected data format'}), 500

        # Obtém os nomes das colunas
        column_names = busca.columns.tolist()

        # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
        consulta_data = busca.to_dict(orient='records')

        return jsonify(consulta_data)


@ColetaProducao_routesJohn.route('/api/JonhField/ExluirColetaProducao', methods=['DELETE'])
@token_required
def delete_ExluirColetaProducao():
    data = request.get_json()
    nomeOperador = data.get('nomeOperador')
    dataFinal = data.get('dataFinal')
    HrFinal = data.get('HrFinal','-')



    consulta = ColetaProducao.ExclusaoColeta(nomeOperador,dataFinal,HrFinal )
    # Obtém os nomes das colunas
    column_names = consulta.columns
    # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
    consulta_data = []
    for index, row in consulta.iterrows():
        consulta_dict = {}
        for column_name in column_names:
            consulta_dict[column_name] = row[column_name]
        consulta_data.append(consulta_dict)
    return jsonify(consulta_data)
