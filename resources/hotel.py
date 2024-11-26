from flask_restful import Resource, reqparse
from sqlalchemy.sql.operators import truediv

from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}       #SELECT * FROM hoteis

#------------------------
class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help= "the field 'nome' connot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'Estrelas' cannot be left blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'},404 #not found


    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 #bad request

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)        #chamando objeto do tipo hotel
        try:                                         #tente salvar
            hotel.save_hotel()
        except:
            return{'message': 'An internal error ocurred trying to save'}, 500      #internal server error
        return hotel.json()



    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)      #funcao para atualizar os dados
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200      #200 -> ok
        hotel = HotelModel(hotel_id, **dados)           #Se o hotel não foi encontrado, cria o hotel
        try:                                         #tente salvar
            hotel.save_hotel()
        except:
            return{'message': 'An internal error ocurred trying to save'}, 500      #internal server error
        return hotel.json(), 201          #created -> criado



    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error ocurre to delete hotel'}, 500          #internal server error
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404