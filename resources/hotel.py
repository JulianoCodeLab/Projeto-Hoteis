from flask_restful import Resource, reqparse
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
class HotelModel:
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self):  # Correção: Adicionado "self" como parâmetro
        return {
            "hotel_id": self.hotel_id,  # Correção: Corrigido de "hortel_id" para "hotel_id"
            "nome": self.nome,
            "estrelas": self.estrelas,
            "diaria": self.diaria,
            "cidade": self.cidade
        }

#-----------------------------------------------------------------------------------------
# Classe Hoteis para lidar com a coleção de hotéis.
class Hoteis(Resource):

    # Método GET para retornar todos os hotéis.
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

    # Método auxiliar para encontrar um hotel pelo ID.
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    # Método GET para retornar um hotel específico pelo ID. Se o hotel não for encontrado, retorna um erro 404.
    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel

        return {'message': 'Hotel not found.'}, 404  # not found

    # Método POST para adicionar um novo hotel. Recebe os dados do hotel via JSON e adiciona à lista de hotéis.
    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args()  # Correção: Usado "argumentos" em vez de "atributos"
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        hoteis.append(novo_hotel)
        return novo_hotel, 201

    # Método PUT para atualizar um hotel existente, ou criar um se ele não existir.
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()  # Correção: Usado "argumentos" em vez de "atributos"
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        hotel = Hotel.find_hotel(hotel_id)

        if hotel:
            hotel.update(novo_hotel)
            return hotel, 200  # ok
        hoteis.append(novo_hotel)
        return novo_hotel, 201  # created

    # Método DELETE para remover um hotel pelo ID.
    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted'}