from flask_restful import Resource

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

class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}

class Hotel(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass