function app() {
    console.log('Aplicação iniciada')
}

async function puxarHerois(nome) {
    if (nome.trim() === '') {
        return [];
    }
    const url = "http://localhost:8000/buscar?nome=" + nome;
    console.log('url definida');
    const response = await axios.get(url);
    console.log('achou herói ' + nome);
    return response.data;
}

async function buscarHerois() {
    
    console.log('Busca iniciada')
    const inputBusca = document.getElementById('inputSearch').value;
    const resultado = await puxarHerois(inputBusca);
    const cardDiv = document.getElementById('cardHeroi');
    cardDiv.innerHTML = '';
    console.log(resultado);

    for (let i = 0; i < resultado.length; i++){
        console.log('for iniciado ' + i)
        let heroi = resultado[i];

        const cardBody = document.createElement('div');
        cardBody.classList.add('col');

        cardBody.innerHTML = `
            <div class="card shadow-sm">
            <img class="bd-placeholder-img card-img-top" width="100%" height="225" src="${heroi.img}" role="img" aria-label="Placeholder: Thumbnail" preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title><rect width="100%" height="100%" fill="#55595c"/></img>

            <div class="card-body">
              <p class="card-text">Nome do heroi: ${heroi.nome}</p>
              <p class="card-text">Alter-ego: ${heroi.alterego}</p>
              <div class="d-flex justify-content-between align-items-center">
                <div class="btn-group">
                  <a type="button" href="detalhes.html" class="btn btn-sm btn-outline-secondary">Visualizar</a>
                </div>
              </div>
            </div>
          </div>
        `;

        cardDiv.appendChild(cardBody)
    }
}

app()