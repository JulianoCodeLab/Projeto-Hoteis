from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin
from flask_jwt_extended import JWTManager       #RESPONSAVEL PELA PARTE DE AUTENTICAÇÃO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'    #pode mudar para qualquer banco, ex postgre atc
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'                 #garante que consegue uma criptografia
api = Api(app)
jwt = JWTManager(app)

@app.before_request
def cria_banco():
    banco.create_all()          #cria banco antes ao rodar (antes da primeira requisição)

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from sql_alchemy import banco   #criando banco automanticamente
    banco.init_app(app)
    app.run(debug=True)