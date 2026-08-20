from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from Backend.Models.data_base import db
from Backend.Models.cliente import Cliente
from Backend.Models.pontos import MovimentacaoPontos, VoucherAbastecimento
from Backend.decorators import cliente_required
from Backend.fidelidade import (
    VOUCHERS_DISPONIVEIS,
    reais_equivalentes,
    regras_fidelidade,
)
import secrets


def gerar_codigo_voucher():
    return f"EZ-{secrets.token_hex(3).upper()}-{secrets.token_hex(2).upper()}"


class PontosController:
    @staticmethod
    def regras():
        return jsonify(regras_fidelidade()), 200

    @cliente_required
    @staticmethod
    def extrato():
        cliente_id = int(get_jwt_identity())
        cliente = Cliente.query.filter_by(id=cliente_id).first()
        if not cliente:
            return jsonify({"mensagem": "Cliente não encontrado!"}), 404

        saldo = cliente.pontos or 0
        historico = (
            MovimentacaoPontos.query
            .filter_by(cliente_id=cliente_id)
            .order_by(MovimentacaoPontos.id.desc())
            .all()
        )
        vouchers = (
            VoucherAbastecimento.query
            .filter_by(cliente_id=cliente_id)
            .order_by(VoucherAbastecimento.id.desc())
            .all()
        )

        return jsonify({
            "pontos": saldo,
            "valor_em_reais": reais_equivalentes(saldo),
            "regras": regras_fidelidade(),
            "historico": [m.para_dicionario() for m in historico],
            "vouchers": [v.para_dicionario() for v in vouchers],
        }), 200

    @cliente_required
    @staticmethod
    def resgatar():
        cliente_id = int(get_jwt_identity())
        cliente = Cliente.query.filter_by(id=cliente_id).first()
        if not cliente:
            return jsonify({"mensagem": "Cliente não encontrado!"}), 404

        dados = request.get_json(silent=True) or {}
        try:
            valor_reais = int(dados.get("valor_reais"))
        except (TypeError, ValueError):
            return jsonify({"mensagem": "Informe o valor do voucher (10, 20 ou 50)."}), 400

        opcao = next((v for v in VOUCHERS_DISPONIVEIS if v["valor_reais"] == valor_reais), None)
        if not opcao:
            return jsonify({"mensagem": "Voucher inválido. Escolha R$ 10, R$ 20 ou R$ 50."}), 400

        pontos_necessarios = opcao["pontos"]
        saldo = cliente.pontos or 0
        if saldo < pontos_necessarios:
            return jsonify({
                "mensagem": f"Pontos insuficientes. Este voucher exige {pontos_necessarios} pontos e você tem {saldo}."
            }), 400

        try:
            cliente.pontos = saldo - pontos_necessarios
            voucher = VoucherAbastecimento(
                cliente_id=cliente_id,
                codigo=gerar_codigo_voucher(),
                valor_reais=opcao["valor_reais"],
                pontos_usados=pontos_necessarios,
                status="Ativo",
            )
            db.session.add(voucher)
            db.session.flush()

            movimento = MovimentacaoPontos(
                cliente_id=cliente_id,
                voucher_id=voucher.id,
                tipo="resgate",
                pontos=-pontos_necessarios,
                descricao=f"Resgate de voucher de abastecimento de R$ {opcao['valor_reais']:.2f}",
            )
            db.session.add(movimento)
            db.session.commit()

            return jsonify({
                "mensagem": "Voucher gerado com sucesso!",
                "pontos": cliente.pontos,
                "valor_em_reais": reais_equivalentes(cliente.pontos),
                "voucher": voucher.para_dicionario(),
            }), 201
        except Exception:
            db.session.rollback()
            return jsonify({"mensagem": "Erro ao resgatar voucher."}), 500
