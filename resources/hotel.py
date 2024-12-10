from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.hotel import HotelModel

class Hoteis(Resource):
    
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}  # SELECT * FROM hoteis


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404  # Not Found

    @jwt_required()  # Atualizado: Adicionado parênteses
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel id '{hotel_id}' already exists."}, 400  # Bad Request

        dados = Hotel.argumentos.parse_args()
        print(dados)    #verificando se os dados estão processados corretamente
        hotel = HotelModel(hotel_id, **dados)  # Criando objeto do tipo Hotel
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error occurred while trying to save.'}, 500  # Internal Server Error
        return hotel.json(), 201  # Created

    @jwt_required()  # Atualizado: Adicionado parênteses
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)  # Atualizando os dados
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200  # OK
        hotel = HotelModel(hotel_id, **dados)  # Caso o hotel não seja encontrado, cria o hotel
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error occurred while trying to save.'}, 500  # Internal Server Error
        return hotel.json(), 201  # Created

    @jwt_required()  # Atualizado: Adicionado parênteses
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error occurred while trying to delete the hotel.'}, 500  # Internal Server Error
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404  # Not Found
