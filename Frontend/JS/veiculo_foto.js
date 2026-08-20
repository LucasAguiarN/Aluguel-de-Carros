function htmlFotoVeiculo(src, alt) {
    if (src) {
        return `<img class="car-photo" src="${src}" alt="${alt || "Veículo"}" onerror="this.outerHTML='<div class=&quot;car-icon&quot;>🚗</div>'">`;
    }
    return `<div class="car-icon">🚗</div>`;
}
