from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'    #pode mudar para qualquer banco, ex postgre atc
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_request
def cria_banco():
    banco.create_all()          #cria banco antes ao rodar (antes da primeira requisição)

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, 'usuarios/<int:user_id>')

if __name__ == '__main__':
    from sql_alchemy import banco   #criando banco automanticamente
    banco.init_app(app)
    app.run(debug=True)