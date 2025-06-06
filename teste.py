import osmnx as ox
import folium

# --- Passo 1: Buscar os dados geográficos do rio ---

# Define o local de interesse.
lugar = "Francisco Beltrão, Paraná, Brazil"
print(f"Buscando dados do Rio Marrecas perto de '{lugar}'...")

# Define as 'tags' para buscar por rios no OpenStreetMap.
tags = {"waterway": "river"}

# Baixa os dados geográficos da área especificada.
# osmnx retorna um GeoDataFrame, uma estrutura de dados que armazena geometrias.
gdf = ox.features_from_place(lugar, tags)

# Filtra o GeoDataFrame para encontrar especificamente o 'Rio Marrecas'.
# Pode haver outros rios na área baixada.
rio_marrecas = gdf[gdf['name'] == 'Rio Marrecas']

# Verifica se o rio foi encontrado.
if rio_marrecas.empty:
    print("Não foi possível encontrar o 'Rio Marrecas' na área especificada.")
    print("Verifique se o nome está correto ou tente uma área maior.")
else:
    print("Rio Marrecas encontrado! Preparando para criar o mapa...")

    # --- Passo 2: Criar o mapa e adicionar o rio ---

    # Pega o ponto central do rio para centralizar o mapa.
    centro_mapa = [rio_marrecas.unary_union.centroid.y, rio_marrecas.unary_union.centroid.x]

    # Cria o objeto do mapa com o ponto central e um nível de zoom inicial.
    mapa = folium.Map(location=centro_mapa, zoom_start=13, tiles="OpenStreetMap")

    # Adiciona um marcador para a cidade, para dar contexto.
    folium.Marker(
        location=centro_mapa,
        popup="<b>Francisco Beltrão</b>",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(mapa)

    # Adiciona o traçado do rio ao mapa.
    # Usamos folium.GeoJson para desenhar a geometria do rio.
    # A função de estilo define a aparência da linha.
    folium.GeoJson(
        rio_marrecas,
        style_function=lambda x: {
            'color': '#007bff',  # Cor azul vibrante
            'weight': 6,         # Espessura da linha
            'opacity': 0.8       # Opacidade da linha
        },
        tooltip='Rio Marrecas' # Texto que aparece ao passar o mouse
    ).add_to(mapa)

    # --- Passo 3: Salvar o mapa como um arquivo HTML ---

    arquivo_saida = "mapa_rio_marrecas.html"
    mapa.save(arquivo_saida)

    print(f"\nMapa salvo com sucesso!")
    print(f"Abra o arquivo '{arquivo_saida}' em seu navegador para ver o resultado.")