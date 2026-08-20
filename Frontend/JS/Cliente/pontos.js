const token = localStorage.getItem("token_cliente");
if (!token) {
    window.location.replace("login.html");
}

function formatarReais(valor) {
    return Number(valor || 0).toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
    });
}

async function carregarPontos() {
    try {
        const response = await fetch(`${API_BASE}/clientes/pontos`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        const dados = await response.json();

        if (!response.ok) {
            throw new Error(dados.mensagem || "Erro ao carregar pontos");
        }

        document.getElementById("saldo_pontos").textContent = dados.pontos;
        document.getElementById("saldo_reais").textContent = formatarReais(dados.valor_em_reais);

        renderizarOpcoes(dados.regras.vouchers, dados.pontos);
        renderizarVouchers(dados.vouchers);
        renderizarHistorico(dados.historico);
    } catch (error) {
        alert(error.message);
    }
}

function renderizarOpcoes(vouchers, saldo) {
    const container = document.getElementById("lista_opcoes_voucher");
    container.innerHTML = "";

    vouchers.forEach((opcao) => {
        const podeResgatar = saldo >= opcao.pontos;
        const card = document.createElement("div");
        card.className = "voucher-card";
        card.innerHTML = `
            <p>⛽ Abastecimento</p>
            <strong>${formatarReais(opcao.valor_reais)}</strong>
            <p>${opcao.pontos} pontos</p>
            <button class="btn-find-cars" style="margin-top: 16px; width: 100%;" ${podeResgatar ? "" : "disabled"}
                onclick="resgatarVoucher(${opcao.valor_reais})">
                ${podeResgatar ? "Resgatar" : "Pontos insuficientes"}
            </button>
        `;
        container.appendChild(card);
    });
}

function renderizarVouchers(vouchers) {
    const container = document.getElementById("lista_vouchers");
    if (!vouchers.length) {
        container.innerHTML = "<p>Você ainda não resgatou nenhum voucher.</p>";
        return;
    }

    container.innerHTML = vouchers.map((v) => `
        <div class="voucher-item">
            <div>
                <div class="voucher-code">${v.codigo}</div>
                <p>${formatarReais(v.valor_reais)} · ${v.pontos_usados} pontos · ${v.status}</p>
            </div>
            <button class="btn-find-cars" onclick="copiarCodigo('${v.codigo}')">Copiar código</button>
        </div>
    `).join("");
}

function renderizarHistorico(historico) {
    const container = document.getElementById("lista_historico");
    if (!historico.length) {
        container.innerHTML = "<p>Nenhuma movimentação ainda. Faça o check-out de uma locação para ganhar pontos.</p>";
        return;
    }

    container.innerHTML = historico.map((item) => {
        const positivo = item.pontos > 0;
        const classe = positivo ? "points-plus" : "points-minus";
        const sinal = positivo ? `+${item.pontos}` : item.pontos;
        return `
            <div class="history-item">
                <div>
                    <p><strong>${item.descricao}</strong></p>
                    <p>${item.criado_em || ""}</p>
                </div>
                <span class="${classe}">${sinal} pts</span>
            </div>
        `;
    }).join("");
}

async function resgatarVoucher(valorReais) {
    if (!confirm(`Confirmar resgate do voucher de abastecimento de ${formatarReais(valorReais)}?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/clientes/pontos/resgatar`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ valor_reais: valorReais }),
        });
        const dados = await response.json();

        if (!response.ok) {
            throw new Error(dados.mensagem || "Erro ao resgatar voucher");
        }

        alert(`Voucher gerado!\nCódigo: ${dados.voucher.codigo}`);
        carregarPontos();
    } catch (error) {
        alert(error.message);
    }
}

function copiarCodigo(codigo) {
    navigator.clipboard.writeText(codigo)
        .then(() => alert("Código copiado: " + codigo))
        .catch(() => alert(codigo));
}

carregarPontos();
