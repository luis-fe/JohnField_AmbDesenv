from flask import Blueprint, jsonify, request
from functools import wraps
from Service import AdicionaisHoraClass
import pandas as pd

from Service.AdicionalHoraClass import AdicionaisHoras

Adicional_routes= Blueprint('Adicional_routes',__name__)  # Esse é o nome atribuido para o conjunto de rotas envolvendo usuario


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token == 'Easy445277888':  # Verifica se o token é igual ao token fixo
            return f(*args, **kwargs)
        return jsonify({'message': 'Acesso negado'}), 401

    return decorated_function


@Adicional_routes.route('/api/JonhField/ConsultarRegistroAdicionaisHr', methods=['GET'])
@token_required
def get_ConsultarRegistroAdicionaisHr():
    dataInicio = request.args.get('dataInicio')
    dataFinal = request.args.get('dataFinal')

    adicional = AdicionaisHoraClass.AdcionalHr(dataInicio, dataFinal)
    busca = adicional.ConsultarAdicionalPerido()

    # Verifica se 'busca' é um DataFrame
    if not isinstance(busca, pd.DataFrame):
        return jsonify({'error': 'Unexpected data format'}), 500

    # Obtém os nomes das colunas
    column_names = busca.columns.tolist()

    # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
    consulta_data = busca.to_dict(orient='records')

    return jsonify(consulta_data)




@Adicional_routes.route('/api/JonhField/InserirRegistroAdicionalHr', methods=['POST'])
@token_required
def salvar_InserirRegistroAdicionalHr():
    data = request.get_json()
    dataInicio = data.get('dataInicio', '-')
    dataFinal = data.get('dataFinal')
    horaInicio = data.get('horaInicio')
    horaFinal = data.get('horaFinal')
    codOperador = data.get('codOperador')
    motivo = data.get('motivo')

    adicional = AdicionaisHoraClass.AdcionalHr(dataInicio, dataFinal, horaInicio, horaFinal, codOperador, motivo)
    consulta = adicional.InserirAdicional()
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


@Adicional_routes.route('/api/JonhField/EditarRegistroAdicionalHr', methods=['PUT'])
@token_required
def PUT_EditarRegistroAdicionalHr():
    data = request.get_json()
    dataInicio = data.get('dataInicio', '-')
    dataFinal = data.get('dataFinal',None)
    horaInicio = data.get('horaInicio')
    horaFinal = data.get('horaFinal',None)
    codOperador = data.get('codOperador')
    motivo = data.get('motivo')

    dataInicioNovo = data.get('dataInicioNovo', '-')
    dataFinalNovo = data.get('dataFinalNovo', '-')
    horaInicioNovo = data.get('horaInicioNovo', '-')
    horaFinaNovo = data.get('horaFinaNovo', '-')

    adicional = AdicionaisHoraClass.AdcionalHr(dataInicio, dataFinal, horaInicio, horaFinal, codOperador, motivo)
    consulta = adicional.UpdateAdicional(dataInicioNovo, dataFinalNovo, horaInicioNovo, horaFinaNovo)
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



@Adicional_routes.route('/api/JonhField/ExcluirRegistroAdicionalHr', methods=['DELETE'])
@token_required
def del_ExcluirRegistroAdicionalHr():
    data = request.get_json()
    dataInicio = data.get('dataInicio')
    dataFinal = data.get('dataFinal', None)
    horaInicio = data.get('horaInicio')
    horaFinal = data.get('horaFinal',None)
    codOperador = data.get('codOperador')
    

    adicional = AdicionaisHoraClass.AdcionalHr(dataInicio, dataFinal, horaInicio, horaFinal, codOperador)
    consulta = adicional.ExcluirAdicional()
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