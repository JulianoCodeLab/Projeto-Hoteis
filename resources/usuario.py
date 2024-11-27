from flask_restful import Resource, reqparse
from sqlalchemy.testing.suite.test_reflection import users

from models.usuario import UserModel


class User(Resource):

#------------- /usuarios/{user_i}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'},404 #not found

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_hotel()
            return {'message': 'user deleted.'}
        return {'message': 'user not found.'}, 404


class UserRegister(Resource):
# ------------- /cadastro
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help= "the field 'login' connot be left brank")
        atributos.add_argument('senha', type=str, required=True, help="the field 'senha' connot be left brank")
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': "the login '{}' already exists.".format(dados['login'])}
        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created sucessfully!'}, 201 #created
