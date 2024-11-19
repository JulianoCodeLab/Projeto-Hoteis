from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.bd' #criando banco de dados direto da raiz
app.config['SQLALCHEMY_TRCK_MODIFICATIONS'] = False

#Antes da primeira requisição ele cria o banco.
@app.before_request
def cria_banco():
    banco.create_all()


api.add_resource(Hoteis, '/hoteis')

api.add_resource(Hotel, '/hoteis/<string:hotel_id>')


if __name__ == '__main__':

    from  sql_alchemy import banco
    banco.init_app(app)

    app.run(debug=True)