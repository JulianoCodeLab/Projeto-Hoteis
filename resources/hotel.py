from flask_restful import Resource, reqparse
from models.hotel   import HotelModel


# Lista inicial de hotéis para servir como base de dados.
hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Santa Catarina'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.9,
        'diaria': 320.20,
        'cidade': 'Santa Catarina'
    }
]

# Classe que representa os hotéis


#-----------------------------------------------------------------------------------------
# Classe Hoteis para lidar com a coleção de hotéis.
class Hoteis(Resource):

    # Metodo GET para retornar todos os hotéis.
    def get(self):
        return {'hoteis': hoteis}
    
#-----------------------------------------------------------------------------------------

# Classe Hotel para lidar com operações relacionadas a um único hotel.
class Hotel(Resource):

    # Definindo construtor | atributos da classe Hotel
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    # Metodo GET para retornar um hotel específico pelo ID. Se o hotel não for encontrado, retorna um erro 404.
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json() # retorna a resposta Json do hotel
        return {'message': 'Hotel not found.'}, 404  # not found

    # Metodo POST para adicionar um novo hotel.
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message' : f'Hotel id "{hotel_id}" already exists.'.format(hotel_id)}, 400 #requisição errada

        dados = Hotel.argumentos.parse_args()  # Correção: Usado "argumentos" em vez de "atributos"
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201 #retorna o hotel criado

    # Metodo PUT para atualizar um hotel existente, ou criar um se ele não existir.
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()  # Correção: Usado "argumentos" em vez de "atributos"
        novo_hotel = HotelModel(hotel_id, **dados)
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            hotel.update(novo_hotel.json())
            return hotel, 200  # ok
        else:
            novo_hotel.save_hotel()
            return novo_hotel, 201  # created

    # Metodo DELETE para remover um hotel pelo ID.
    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted'}