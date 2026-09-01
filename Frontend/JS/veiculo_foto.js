function htmlFotoVeiculo(src, alt) {
    if (src) {
        return `<img class="car-photo" src="${src}" alt="${alt || "Veículo"}" onerror="this.outerHTML='<div class=&quot;car-icon&quot;>🚗</div>'">`;
    }
    return `<div class="car-icon">🚗</div>`;
}

function htmlEstrelasSomenteLeitura(nota) {
    let estrelas = '';
    for (let i = 1; i <= 5; i++) {
        estrelas += `<span class="star${i <= nota ? ' selected' : ''}">★</span>`;
    }
    return `<div class="stars-input stars-readonly">${estrelas}</div>`;
}

function formatarDataAvaliacao(criadoEm) {
    if (!criadoEm) return '';
    const dataParte = criadoEm.split(' ')[0];
    return dataParte.split('-').reverse().join('/');
}

async function verAvaliacoes(veiculoId) {
    const existente = document.getElementById('modal_avaliacoes_veiculo');
    if (existente) existente.remove();

    try {
        const resp = await fetch(`${API_BASE}/veiculos/${veiculoId}/avaliacoes`);
        const dados = await resp.json();

        const mediaTxt = dados.media != null ? dados.media.toFixed(1).replace('.', ',') : '—';
        const totalTxt = dados.total === 1 ? '1 avaliação' : `${dados.total} avaliações`;

        const itensHtml = dados.avaliacoes.length
            ? dados.avaliacoes.map(a => `
                <div class="avaliacao-item">
                    ${htmlEstrelasSomenteLeitura(a.nota)}
                    <p class="avaliacao-comentario">${a.comentario ? a.comentario : '<em>Sem comentário</em>'}</p>
                    <span class="avaliacao-data">${formatarDataAvaliacao(a.criado_em)}</span>
                </div>
            `).join('')
            : '<p>Nenhuma avaliação ainda.</p>';

        const overlay = document.createElement('div');
        overlay.id = 'modal_avaliacoes_veiculo';
        overlay.className = 'modal-overlay';
        overlay.innerHTML = `
            <div class="modal-box modal-avaliacoes">
                <div class="modal-avaliacoes-header">
                    <h3>★ ${mediaTxt} <span class="modal-avaliacoes-total">(${totalTxt})</span></h3>
                    <button class="btn-secondary" onclick="document.getElementById('modal_avaliacoes_veiculo').remove()">Fechar</button>
                </div>
                <div class="modal-avaliacoes-lista">
                    ${itensHtml}
                </div>
            </div>
        `;
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) overlay.remove();
        });
        document.body.appendChild(overlay);
    } catch (error) {
        console.error('Erro ao buscar avaliações:', error);
        alert('Não foi possível carregar as avaliações.');
    }
}
