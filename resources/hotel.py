from flask_restful import Resource, reqparse
from models.hotel import HotelModel


hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hoteis',
        'estrelas': '4.3',
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
            'hotel_id': 'bravo',
            'nome': 'Bravo Hoteis',
            'estrelas': '4.4',
            'diaria': 380.90,
            'cidade': 'Santa Catarina'
    },
    {
            'hotel_id': 'charlie',
            'nome': 'Charlie Hoteis',
            'estrelas': '3.9',
            'diaria':320.20,
            'cidade': 'Santa Catarina'
    },
]


#-----------------------
class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}

#------------------------
class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found.'},404 #not found


    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 #bad request

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)        #chamando objeto do tipo hotel
        hotel.save_hotel()
        return hotel.json()



    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)  # chamando objeto do tipo hotel
        novo_hotel = hotel_objeto.json()  # transformando o novo objeto em json
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)    #funcao para atualizar os dados
            return novo_hotel, 200      #200 -> ok
        hoteis.append(novo_hotel)
        return novo_hotel, 201          #created -> criado

    def delete(self, hotel_id):
        global hoteis

        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted.'}