document.addEventListener("DOMContentLoaded", () => {
    const cep = document.getElementById("cep");
    if (cep) {
        cep.addEventListener("change", () => buscar_endereco());
    }
});

function validar_dados() {
    let nome = document.getElementById("nome").value.trim();
    let email = document.getElementById("email").value.trim();
    let cpf = document.getElementById("cpf").value.trim();
    let senha = document.getElementById("senha").value;
    let celular = document.getElementById("celular").value.trim();
    let cep = document.getElementById("cep").value.trim();
    let endereco = document.getElementById("endereco").value.trim();
    let numero = document.getElementById("numero").value;

    if (!nome || !email || !cpf || !senha || !celular || !cep || !endereco || !numero) {
        alert("Preencha todos os campos!");
        return;
    }

    enviar_cadastro(nome, email, cpf, senha, celular, cep, endereco, numero);
}

async function buscar_endereco() {
    let cep = document.getElementById("cep").value.replace(/\D/g, "");
    if (cep.length !== 8) {
        return;
    }
    try {
        let request = await fetch("https://viacep.com.br/ws/" + cep + "/json/");
        if (!request.ok) {
            throw new Error("Erro ao buscar CEP");
        }
        let resposta = await request.json();
        if (resposta.erro || resposta.logradouro == undefined) {
            alert("CEP Inválido!");
            document.getElementById("cep").value = "";
        } else {
            document.getElementById("endereco").value = resposta.logradouro;
        }
    } catch (error) {
        console.log(error);
    }
}

async function enviar_cadastro(nome, email, cpf, senha, celular, cep, endereco, numero) {
    let complemento = document.getElementById("complemento").value;
    const botao = document.querySelector("form .btn");
    const textoOriginal = botao ? botao.textContent : "";

    if (botao) {
        botao.disabled = true;
        botao.textContent = "Cadastrando...";
    }

    let dados = {
        nome: nome,
        cpf: cpf,
        email: email,
        senha: senha,
        celular: celular,
        cep: cep,
        endereco: endereco,
        numero: numero,
        complemento: complemento
    };

    try {
        let response = await fetch(`${API_BASE}/clientes`, {
            method: "POST",
            body: JSON.stringify(dados),
            headers: {
                "Content-Type": "application/json"
            },
            signal: AbortSignal.timeout(15000)
        });

        let resposta = await response.json();

        if (!response.ok) {
            throw new Error(resposta.mensagem || "Erro ao cadastrar cliente");
        }

        alert("Cadastro realizado com sucesso!");
        window.location.href = "../../pages/Cliente/login.html";

    } catch (error) {
        console.error("Erro:", error);
        if (error.name === "TimeoutError" || error.name === "AbortError" || error.message === "Failed to fetch") {
            alert("Não foi possível conectar à API. Confirme se o backend está rodando em http://127.0.0.1:5000");
        } else {
            alert(error.message);
        }
    } finally {
        if (botao) {
            botao.disabled = false;
            botao.textContent = textoOriginal || "Criar Conta";
        }
    }
}
