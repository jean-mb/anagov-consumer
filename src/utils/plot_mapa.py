import gmplot
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def plotar_estacoes(estacoes): 
    items = estacoes
    estacoes_filtradas = []
    for item in items:
        if item["Operando"] == "1":
            try:
                lat = float(item['Latitude'])
                lng = float(item['Longitude'])
                nome = item['codigoestacao']
                tipo = item['Tipo_Estacao']
                estacoes_filtradas.append((lat, lng, nome, tipo))
            except (ValueError, TypeError):
                continue

    gmap = gmplot.GoogleMapPlotter(estacoes_filtradas[0][0], estacoes_filtradas[0][1], 10, apikey=GOOGLE_API_KEY)

    for lat, lng, title, tipo in estacoes_filtradas:
        if tipo == "Fluviometrica":
            gmap.marker(lat, lng, title=title, color='red')
        elif tipo == "Pluviometrica":
            gmap.marker(lat, lng, title=title, color='blue')
        
    mapa_path = "html/index.html"
    gmap.draw(mapa_path)
    script_cru = '''
    setTimeout(function() {
        console.log('Mapa carregado');
        document.querySelectorAll('div[role="img"]').forEach(function(div) {
            div.addEventListener('click', function() {
                const title = div.getAttribute('title') || 'Sem título';
                navigator.clipboard.writeText(title).then(function() {
                    alert('Código da estação copiado: ' + title);
                }, function(err) {
                    console.error('Erro ao copiar: ', err);
                });
            });
        });
    }, 5000);
    '''
    with open(mapa_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    script_onclick = soup.new_tag('script', type='text/javascript')
    script_onclick.string = script_cru

    if soup.body:
        soup.body.append(script_onclick)
    else:
        print("A tag <body> não foi encontrada no arquivo HTML.")

    with open(mapa_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"Mapa gerado com sucesso: {mapa_path}")