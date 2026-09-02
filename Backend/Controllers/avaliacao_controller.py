from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

from Backend.Models.data_base import db
from Backend.Models.avaliacao import Avaliacao
from Backend.Models.reserva import Reserva
from Backend.Models.cliente import Cliente
from Backend.Models.veiculo import Veiculo
from Backend.Models.pontos import MovimentacaoPontos
from Backend.decorators import cliente_required
from Backend.fidelidade import PONTOS_AVALIACAO


class AvaliacaoController:
    @cliente_required
    @staticmethod
    def criar_avaliacao(reserva_id):
        cliente_id = int(get_jwt_identity())

        reserva = Reserva.query.filter_by(id=reserva_id, cliente_id=cliente_id).first()
        if not reserva:
            return jsonify({"mensagem": "Reserva não encontrada ou acesso não autorizado."}), 404

        if reserva.status != "Concluído":
            return jsonify({"mensagem": "Só é possível avaliar reservas já concluídas."}), 400

        if Avaliacao.query.filter_by(reserva_id=reserva_id).first():
            return jsonify({"mensagem": "Essa reserva já foi avaliada."}), 409

        dados = request.get_json(silent=True) or {}
        nota = dados.get("nota")
        comentario = (dados.get("comentario") or "").strip() or None

        try:
            nota_int = int(nota)
        except (TypeError, ValueError):
            return jsonify({"mensagem": "Informe uma nota de 1 a 5."}), 400

        if nota_int < 1 or nota_int > 5:
            return jsonify({"mensagem": "A nota precisa ser entre 1 e 5."}), 400

        try:
            avaliacao = Avaliacao(
                reserva_id=reserva.id,
                cliente_id=cliente_id,
                veiculo_id=reserva.veiculo_id,
                nota=nota_int,
                comentario=comentario,
            )
            db.session.add(avaliacao)

            cliente = Cliente.query.filter_by(id=cliente_id).first()
            if cliente:
                cliente.pontos = (cliente.pontos or 0) + PONTOS_AVALIACAO
                veiculo = Veiculo.query.filter_by(id=reserva.veiculo_id).first()
                veiculo_nome = f"{veiculo.marca} {veiculo.modelo}" if veiculo else "veículo"
                db.session.add(MovimentacaoPontos(
                    cliente_id=cliente_id,
                    reserva_id=reserva.id,
                    tipo="credito",
                    pontos=PONTOS_AVALIACAO,
                    descricao=f"Avaliação da locação de {veiculo_nome}",
                ))

            db.session.commit()
        except Exception:
            db.session.rollback()
            return jsonify({"mensagem": "Erro ao registrar avaliação."}), 500

        return jsonify({
            "mensagem": "Avaliação registrada com sucesso!",
            "avaliacao": avaliacao.para_dicionario(),
            "pontos_ganhos": PONTOS_AVALIACAO,
        }), 201

    @staticmethod
    def listar_avaliacoes_veiculo(veiculo_id):
        avaliacoes = (
            Avaliacao.query
            .filter_by(veiculo_id=veiculo_id)
            .order_by(Avaliacao.id.desc())
            .all()
        )

        total = len(avaliacoes)
        media = round(sum(a.nota for a in avaliacoes) / total, 1) if total else None

        return jsonify({
            "media": media,
            "total": total,
            "avaliacoes": [a.para_dicionario() for a in avaliacoes],
        }), 200
