from flask import Blueprint, jsonify, request
from functools import wraps
from Service.Operacoes import Opercao
import pandas as pd
operacao_routesJohn = Blueprint('operacaoJohn', __name__) # Esse é o nome atribuido para o conjunto de rotas envolvendo usuario

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token == 'Easy445277888':  # Verifica se o token é igual ao token fixo
            return f(*args, **kwargs)
        return jsonify({'message': 'Acesso negado'}), 401

    return decorated_function

@operacao_routesJohn.route('/api/JonhField/BuscarOperacoes', methods=['GET'])
@token_required
def get_BuscarOperacoes():
    try:
        print('Minha Api 1')
        busca = Opercao.Buscar_Operacoes()

        # Verifica se 'busca' é um DataFrame
        if not isinstance(busca, pd.DataFrame):
            return jsonify({'error': 'Unexpected data format'}), 500

        # Obtém os nomes das colunas
        column_names = busca.columns.tolist()

        # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
        consulta_data = busca.to_dict(orient='records')

        return jsonify(consulta_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@operacao_routesJohn.route('/api/JonhField/InserirOperacao', methods=['POST'])
@token_required
def InserirOperacao():
    data = request.get_json()
    nomeOperacao = data.get('nomeOperacao')
    nomeFase = data.get('nomeFase')
    Maq_Equipamento = data.get('Maq_Equipamento')
    nomeCategoria = data.get('nomeCategoria','-')
    tempoPadrao = data.get('tempoPadrao','-')

    consulta = Opercao.InserirOperacao(nomeOperacao, nomeFase, Maq_Equipamento, nomeCategoria, tempoPadrao )
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

@operacao_routesJohn.route('/api/JonhField/AtualizarOperacao', methods=['PUT'])
@token_required
def AtualizarOperacao():
    data = request.get_json()
    codOperacao = data.get('codOperacao')
    nomeOperacao = data.get('nomeOperacao','-')
    nomeFase = data.get('nomeFase','-')
    Maq_Equipamento = data.get('Maq_Equipamento','-')
    nomeCategoria = data.get('nomeCategoria','-')
    tempoPadrao = data.get('tempoPadrao','-')


    consulta = Opercao.UpdateOperacao(codOperacao, nomeOperacao, nomeFase, Maq_Equipamento, nomeCategoria, tempoPadrao)
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