import gmplot
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def plotar_estacoes(estacoes_filtradas, estacoes_original, mostrar_todas=False): 
    items = estacoes_original
    ids_estacoes_filtradas = [item['codigoestacao'] for item in estacoes_filtradas]
    estacoes_plotagem = []
    for item in items:
        if item["Operando"] == "1":
            try:
                lat = float(item['Latitude'])
                lng = float(item['Longitude'])
                codigo = item['codigoestacao']
                tipo = item['Tipo_Estacao']
                estacoes_plotagem.append((lat, lng, codigo, tipo))
            except (ValueError, TypeError):
                continue

    gmap = gmplot.GoogleMapPlotter(estacoes_plotagem[0][0], estacoes_plotagem[0][1], 10, apikey=GOOGLE_API_KEY)

    for lat, lng, codigo, tipo in estacoes_plotagem:

        if tipo == "Fluviometrica":
            if codigo in ids_estacoes_filtradas:
                gmap.marker(lat, lng, title=codigo, label="", color='red')
            elif mostrar_todas:
                gmap.marker(lat, lng, title=codigo, label="", color="pink") 
        elif tipo == "Pluviometrica":
            if codigo in ids_estacoes_filtradas:
                gmap.marker(lat, lng, title=codigo,label="", color='blue')
            elif mostrar_todas:
                gmap.marker(lat, lng, title=codigo,label="", color="azure") 
    mapa_path = "html/index.html"
    gmap.draw(mapa_path)
    script_cru = '''
    setTimeout(function() {
        console.log('Mapa carregado');
        var marcadores = 0;
        document.querySelectorAll('div[role="img"]').forEach(function(div) {
            marcadores++;
            div.addEventListener('click', function() {
                const title = div.getAttribute('title') || 'Sem título';
                navigator.clipboard.writeText(title).then(function() {
                    alert('Código da estação copiado: ' + title);
                }, function(err) {
                    console.error('Erro ao copiar: ', err);
                });
            });
        });
        console.log('Total de marcadores:', marcadores);
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