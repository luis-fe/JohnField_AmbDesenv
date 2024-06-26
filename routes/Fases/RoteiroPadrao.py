from flask import Blueprint, jsonify, request
from functools import wraps
from Service import RoteiroPadrao
import pandas as pd
roteiroPadrao_routesJohn = Blueprint('RoteiroJohn', __name__) # Esse é o nome atribuido para o conjunto de rotas envolvendo usuario

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token == 'Easy445277888':  # Verifica se o token é igual ao token fixo
            return f(*args, **kwargs)
        return jsonify({'message': 'Acesso negado'}), 401

    return decorated_function

@roteiroPadrao_routesJohn.route('/api/JonhField/InserirRoteiroPadrao', methods=['POST'])
@token_required
def InserirRoteiroPadrao():
    data = request.get_json()
    codRoteiro = data.get('codRoteiro')
    nomeRoteiro = data.get('nomeRoteiro')
    arrayFases = data.get('arrayFases')

    consulta = RoteiroPadrao.InserirRoteiroPadrao(codRoteiro, nomeRoteiro, arrayFases )
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


@roteiroPadrao_routesJohn.route('/api/JonhField/AtualizarRoteiroPadrao', methods=['PUT'])
@token_required
def AtualizarRoteiroPadrao():
    data = request.get_json()
    codRoteiro = data.get('codRoteiro')
    nomeRoteiro = data.get('nomeRoteiro')
    arrayFases = data.get('arrayFases')

    consulta = RoteiroPadrao.UpdateRoteiro(codRoteiro, nomeRoteiro, arrayFases)
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

@roteiroPadrao_routesJohn.route('/api/JonhField/BuscarRoteiros', methods=['GET'])
@token_required
def BuscarRoteiros():


    consulta = RoteiroPadrao.BuscarRoteiros()
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