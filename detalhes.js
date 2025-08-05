function app() {
    console.log('Aplicação iniciada.')
    preencherDetalhes()
}

function obterIdHeroi() {
    const urlParams = new URLSearchParams(window.location.search);
    const idHeroi = urlParams.get('id');
    return idHeroi;
}

async function obterInformacoesHeroi() {
    const url = "http://localhost:8000/detalhes-heroi?id=" + obterIdHeroi();
    const response = await axios.get(url);
    return response.data;
}

async function preencherDetalhes() {
    const heroi = await obterInformacoesHeroi();

    const nomeDiv = document.getElementById('nomeHeroi');
    nomeDiv.innerHTML = `<h1 class="fw-light">Detalhes sobre: ${heroi.alterego}</h1>
    <img class="bd-placeholder-img" width="225" height="225" src="${heroi.img}" role="img" aria-label="Placeholder: Thumbnail" preserveAspectRatio="xMidYMid slice" focusable="false"></img>`;

    const conteudoDiv = document.getElementById('heroiTabContent');
    conteudoDiv.innerHTML = `
            <div class="tab-pane fade show active p-3" id="estatisticas" role="tabpanel" aria-labelledby="estatisticas-tab">
                <h4>Estatísticas</h4>
                <p>Inteligência: ${heroi.poderes.intelligence}<br>
                Força: ${heroi.poderes.strength}<br>
                Velocidade: ${heroi.poderes.speed}<br>
                Durabilidade: ${heroi.poderes.durability}<br>
                Poder: ${heroi.poderes.power}<br>
                Combate: ${heroi.poderes.combat}</p>
              </div>
              <div class="tab-pane fade p-3" id="biografia" role="tabpanel" aria-labelledby="biografia-tab">
                <h4>Biografia</h4>
                <p>Nome completo: ${heroi["biografia"]["full-name"]}<br>
                Alter-egos: ${heroi["biografia"]["alter-egos"]}<br>
                Pseudônimos: ${heroi["biografia"]["aliases"]}<br>
                Local de Nascimento: ${heroi["biografia"]["place-of-birth"]}<br>
                Primeira Aparição:: ${heroi["biografia"]["first-appearance"]}<br>
                Editora: ${heroi["biografia"]["publisher"]}<br>
                Vies: ${heroi["biografia"]["alignment"]}</p>
              </div>
              <div class="tab-pane fade p-3" id="aparencia" role="tabpanel" aria-labelledby="aparencia-tab">
                <h4>Aparência</h4>
                <p>Gênero: ${heroi.aparencia.gender}<br>
                Raça: ${heroi.aparencia.race}<br>
                Altura: ${heroi.aparencia.height[1]}<br>
                Peso: ${heroi.aparencia.weight[1]}<br>
                Cor do Olho: ${heroi.aparencia["eye-color"]}<br>
                Cor do Cabelo: ${heroi.aparencia["hair-color"]}</p>
              </div>
              <div class="tab-pane fade p-3" id="carreira" role="tabpanel" aria-labelledby="carreira-tab">
                <h4>Carreira</h4>
                <p>Ocupação: ${heroi.carreira.occupation}<br>
                Base: ${heroi.carreira.base}</p>
              </div>
              <div class="tab-pane fade p-3" id="conexoes" role="tabpanel" aria-labelledby="conexoes-tab">
                <h4>Conexões</h4>
                <p>Afiliações: ${heroi.conexoes["group-affiliation"]}<br>
                Relativos: ${heroi.conexoes.relatives}</p>
              </div>
    `;
    console.log("Detalhes preenchidos com sucesso!")
}

app()