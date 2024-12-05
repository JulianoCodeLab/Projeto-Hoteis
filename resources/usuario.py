from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required
import hmac #subistituto para safe_str_cmp

from models.usuario import UserModel

# Parser de argumentos para login e senha
atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank.")

class User(Resource):
    """Classe para manipular usuários individuais."""

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404  # Not Found

    @jwt_required()  # Atualização: Adicionado parênteses
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404


class UserRegister(Resource):
    """Classe para registrar novos usuários."""

    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': f"The login '{dados['login']}' already exists."}, 400  # Bad Request
        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created successfully!'}, 201  # Created


class UserLogin(Resource):
    """Classe para login de usuários e criação de tokens."""


    @classmethod
    def post(cls):

        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and hmac.compare_digest(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200  # OK
        return {'message': 'The username or password is incorrect.'}, 401  # Unauthorized
