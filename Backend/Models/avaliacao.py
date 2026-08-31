from datetime import datetime
from .data_base import db


class Avaliacao(db.Model):
    __tablename__ = "avaliacoes"

    id = db.Column(db.Integer, primary_key=True)
    reserva_id = db.Column(db.Integer, db.ForeignKey("reservas.id"), nullable=False, unique=True, index=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False, index=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey("veiculos.id"), nullable=False, index=True)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(500), nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def para_dicionario(self):
        return {
            "id": self.id,
            "reserva_id": self.reserva_id,
            "nota": self.nota,
            "comentario": self.comentario,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S") if self.criado_em else None,
        }
