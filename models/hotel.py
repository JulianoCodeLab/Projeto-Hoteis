from sqlalchemy import Float, String, Numeric
from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(String(50), primary_key=True)  # Alterado para String com comprimento específico
    nome = banco.Column(String(80))  # Coluna nome, agora String(80)
    estrelas = banco.Column(Float)  # Coluna estrelas, agora Float
    diaria = banco.Column(Numeric(10, 2))  # Coluna diaria, alterado para Numeric para controlar a precisão
    cidade = banco.Column(String(40))  # Coluna cidade, agora String(40)

    # Construtor
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    # Transformando objeto em dicionário
    def json(self):
        return {
            "hotel_id": self.hotel_id,
            "nome": self.nome,
            "estrelas": self.estrelas,
            "diaria": str(self.diaria),  # Convertendo para string para evitar problemas com o formato
            "cidade": self.cidade
        }

    # Método auxiliar para encontrar um hotel pelo ID.
    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()  # SELECT * FROM hoteis WHERE hotel_id = hotel_id
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()
