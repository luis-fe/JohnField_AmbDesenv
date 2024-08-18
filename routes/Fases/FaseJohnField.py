from flask import Blueprint, jsonify, request
from functools import wraps
from Service import FaseJohnField, faseClass
import pandas as pd

fase_routesJohn = Blueprint('FaseJohn', __name__) # Esse é o nome atribuido para o conjunto de rotas envolvendo usuario

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token == 'Easy445277888':  # Verifica se o token é igual ao token fixo
            return f(*args, **kwargs)
        return jsonify({'message': 'Acesso negado'}), 401

    return decorated_function

@fase_routesJohn.route('/api/JonhField/Fases', methods=['GET'])
@token_required
def Fases_jonh_field():
    consulta = FaseJohnField.BuscarFases()
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

@fase_routesJohn.route('/api/JonhField/FasesInicial', methods=['GET'])
@token_required
def FasesInicial():
    consulta = FaseJohnField.BuscarFasesTipoInicial()
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


@fase_routesJohn.route('/api/JonhField/NovaFase', methods=['POST'])
@token_required
def NovaFase():
    data = request.get_json()
    codFase = data.get('codFase')
    nomeFase = data.get('nomeFase', '-')
    FaseInical = data.get('FaseInical?')
    FaseFinal = data.get('FaseFinal?')
    ObrigaInformaTamCor = data.get("ObrigaInformaTamCor?")
    LeadTime = data.get("LeadTime",0)

    consulta = FaseJohnField.InserirFase(codFase, nomeFase,FaseInical,FaseFinal,ObrigaInformaTamCor,LeadTime)
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

@fase_routesJohn.route('/api/JonhField/AlterarFase', methods=['PUT'])
@token_required
def AlterarFase():
    data = request.get_json()
    codFase = data.get('codFase')
    nomeFase = data.get('nomeFase', '-')
    FaseInical = data.get('FaseInical?')
    FaseFinal = data.get('FaseFinal?')
    ObrigaInformaTamCor = data.get("ObrigaInformaTamCor?")
    LeadTime = data.get("LeadTime",0)


    consulta = FaseJohnField.UpdateFase(codFase, nomeFase,FaseInical,FaseFinal,ObrigaInformaTamCor,LeadTime)
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