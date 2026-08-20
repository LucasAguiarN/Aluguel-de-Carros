from datetime import datetime
from .data_base import db


class MovimentacaoPontos(db.Model):
    __tablename__ = "movimentacoes_pontos"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False, index=True)
    reserva_id = db.Column(db.Integer, db.ForeignKey("reservas.id"), nullable=True)
    voucher_id = db.Column(db.Integer, db.ForeignKey("vouchers_abastecimento.id"), nullable=True)
    tipo = db.Column(db.String(20), nullable=False)
    pontos = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def para_dicionario(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "pontos": self.pontos,
            "descricao": self.descricao,
            "reserva_id": self.reserva_id,
            "voucher_id": self.voucher_id,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S") if self.criado_em else None,
        }


class VoucherAbastecimento(db.Model):
    __tablename__ = "vouchers_abastecimento"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False, index=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False, index=True)
    valor_reais = db.Column(db.Float, nullable=False)
    pontos_usados = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Ativo")
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def para_dicionario(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "valor_reais": self.valor_reais,
            "pontos_usados": self.pontos_usados,
            "status": self.status,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S") if self.criado_em else None,
        }
