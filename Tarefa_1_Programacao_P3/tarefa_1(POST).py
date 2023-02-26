import math

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['POST'])
def calculate_age():
    """
    Calcula a idade de uma pessoa em uma data futura e retorna um json
    com o nome, idade atual e idade futura como resposta para a requisição.
    Returns:
        response: json
    """
    data = request.get_json()

    name = data['name']

    # Verifica se o nome foi informado
    if not name:
        return jsonify({'error': 'Dados incompletos, o nome deve ser informado'}), 400
    
    # Verifica se a data de nascimento foi informada
    try:
        birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
    except:
        return jsonify({'error': 'Dados incompletos, a data aniversário deve ser informado'}), 400
    
    # Verifica se a data futura foi informada
    try:
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except:
        return jsonify({'error': 'Dados incompletos, a data deve ser informada'}), 400
    
    # Verifica se a data futura é maior do que a data atual
    if date < datetime.now().date():
        return jsonify({'error': 'A data deve ser maior do que o dia atual,' \
            'coloque uma data futura'}), 400
    
    age_now = (datetime.now().date() - birthdate).days/365
    
    age_then = (date - birthdate).days/365

    age_now = math.trunc(age_now)
    age_then = math.trunc(age_then)
    
    msg = f"Olá, {name}! Você tem {age_now} anos e em {date.strftime('%d/%m/%Y')} você terá {age_then} anos."
    
    response = {
        "quote": msg,
        "ageNow": age_now,
        "ageThen": age_then
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False)
