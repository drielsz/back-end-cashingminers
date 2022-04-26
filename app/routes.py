from msilib.schema import Error
from flask import request, jsonify, redirect, url_for
from app import app
from app.controllers.usercontroller import authentication, create_user
from app.utils.secury import create_token
from sqlalchemy.exc import IntegrityError
import asyncio

from app.database.schemas import (
    User, user_schema,
)

loop = asyncio.get_event_loop()

@app.route('/')
def home():
    return jsonify(message='Hello')

@app.route('/login', methods=['POST',])
def login():
  data = request.json
  
  # Verificando se todos os campos foram preenchidos
  if( data.get('email') and data.get('password') ):
    auth = loop.run_until_complete(authentication(data['email'], data['password']))
      
    if( auth is not None and len(auth) > 0 ):
      auth = user_schema.dump(auth)
      token = create_token(auth)
      
      return jsonify(token=token), 200 
    
    return jsonify(message="E-mail e/ou senha incorretos!"), 400 
  
  return jsonify(message="Preencha todos os campos!"), 422 

@app.route('/register', methods=['POST',])
def create_account():
  data = request.json

  # Verificando se todos os campos foram preenchidos
  if( data.get('name') and data.get('email') and data.get('password') and data.get('password_again') ):
    if( data.get('password') == data.get('password_again') ):
      # Criando uma instância do usuário
      new_user = User(name=data['name'], email=data['email'], password=data['password'])

      try: # tentando criar o usuário
        user_uuid = loop.run_until_complete( create_user(new_user) )

        return jsonify(user_uuid=user_uuid), 201 # Created
      except Exception as e: # Erro de integridade
        print (e)
        return jsonify(message="Esse e-mail já está em uso, tente novamente utilizando outro!"), 400 # Bad Request

    return jsonify(message="As senhas não coincidem, tente novamente!"), 400 # Bad Request

  return jsonify(message="Preencha todos os campos"), 422 # Unprocessable Entity