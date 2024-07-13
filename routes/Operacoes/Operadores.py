from flask import Blueprint, jsonify, request
from functools import wraps
from Service.Operacoes import Operadores
import pandas as pd
operador_routesJohn = Blueprint('operadorJohn', __name__) # Esse é o nome atribuido para o conjunto de rotas envolvendo usuario

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token == 'Easy445277888':  # Verifica se o token é igual ao token fixo
            return f(*args, **kwargs)
        return jsonify({'message': 'Acesso negado'}), 401

    return decorated_function

@operador_routesJohn.route('/api/JonhField/Operadores', methods=['GET'])
@token_required
def get_Operadores():
    try:

        busca = Operadores.ConsultarOperadores()

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


@operador_routesJohn.route('/api/JonhField/ConsultaEscalaTrabalho', methods=['GET'])
@token_required
def get_ConsultaEscalaTrabalho():
    try:

        busca = Operadores.ConsultaEscalaTrabalho()

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
@operador_routesJohn.route('/api/JonhField/NovoOperador', methods=['POST'])
@token_required
def getNovoOperador():
    data = request.get_json()
    codOperador = data.get('codOperador','-')
    nomeOperador = data.get('nomeOperador')
    Escala = data.get('Escala')


    consulta = Operadores.InserirOperador(nomeOperador, Escala )
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

@operador_routesJohn.route('/api/JonhField/NovaEscalaTrabalho', methods=['POST'])
@token_required
def postNovaEscalaTrabalho():
    data = request.get_json()
    nomeEscala = data.get('nomeEscala')
    descricaoPeriodo1 = data.get('descricaoPeriodo1')
    inicio_periodo1 = data.get('inicio_periodo1')
    termino_periodo1 = data.get('termino_periodo1')
    descricaoPeriodo2 = data.get('descricaoPeriodo2')
    inicio_periodo2 = data.get('inicio_periodo2')
    termino_periodo2 = data.get('termino_periodo2')
    descricaoPeriodo3 = data.get('descricaoPeriodo3')
    inicio_periodo3 = data.get('inicio_periodo3')
    termino_periodo3 = data.get('termino_periodo3')


    consulta = Operadores.InserirEscalaTrabalho(nomeEscala, descricaoPeriodo1 , inicio_periodo1, termino_periodo1,
                          descricaoPeriodo2 , inicio_periodo2, termino_periodo2,
                          descricaoPeriodo3 , inicio_periodo3, termino_periodo3)
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

@operador_routesJohn.route('/api/JonhField/AlterarOperador', methods=['PUT'])
@token_required
def AtualizarOperador():
    data = request.get_json()
    codOperador = data.get('codOperador')
    nomeOperador = data.get('nomeOperador','-')
    Escala = data.get('Escala','-')


    consulta = Operadores.AtualizandoOperador(codOperador, nomeOperador, Escala)
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


@operador_routesJohn.route('/api/JonhField/AlterarEscalaTrabalho', methods=['PUT'])
@token_required
def postAlterarEscalaTrabalho():
    data = request.get_json()
    nomeEscalaAtual = data.get('nomeEscalaAtual')
    nomeEscalaNova = data.get('nomeEscalaNova','-')
    descricaoPeriodo1 = data.get('descricaoPeriodo1','-')
    inicio_periodo1 = data.get('inicio_periodo1','-')
    termino_periodo1 = data.get('termino_periodo1','-')
    descricaoPeriodo2 = data.get('descricaoPeriodo2','-')
    inicio_periodo2 = data.get('inicio_periodo2','-')
    termino_periodo2 = data.get('termino_periodo2','-')
    descricaoPeriodo3 = data.get('descricaoPeriodo3','-')
    inicio_periodo3 = data.get('inicio_periodo3','-')
    termino_periodo3 = data.get('termino_periodo3','-')


    consulta = Operadores.AtualizarEscalaTrabalho(nomeEscalaAtual,nomeEscalaNova, descricaoPeriodo1 , inicio_periodo1, termino_periodo1,
                          descricaoPeriodo2 , inicio_periodo2, termino_periodo2,
                          descricaoPeriodo3 , inicio_periodo3, termino_periodo3)
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