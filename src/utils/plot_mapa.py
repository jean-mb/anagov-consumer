import folium
import geopandas
import pandas as pd
from shapely.geometry import Point
import osmnx as ox

def plotar_estacoes(estacoes_filtradas, estacoes_original, mostrar_todas=False, cidade_contexto=None, output_path="html/index.html"):
    ids_estacoes_filtradas = {item['codigoestacao'] for item in estacoes_filtradas}
    
    dados_plotagem = []
    for item in estacoes_original:
        if item.get("Operando") == "1":
            try:
                lat = float(item['Latitude'])
                lng = float(item['Longitude'])
                codigo = item['codigoestacao']
                tipo = item['Tipo_Estacao']
                dados_plotagem.append({
                    'codigo': codigo,
                    'tipo': tipo,
                    'latitude': lat,
                    'longitude': lng,
                    'geometry': Point(lng, lat)
                })
            except (ValueError, TypeError, KeyError):
                continue

    if not dados_plotagem:
        print("Nenhuma estação válida para plotar.")
        return

    gdf = geopandas.GeoDataFrame(dados_plotagem, crs="EPSG:4326")

    map_center = [gdf['latitude'].mean(), gdf['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=9, tiles="OpenStreetMap")

    if cidade_contexto:
        try:
            area = ox.geocode_to_gdf(cidade_contexto)
            folium.GeoJson(
                area,
                name=f"Contorno de {cidade_contexto.split(',')[0]}",
                style_function=lambda x: {'color': 'black', 'weight': 2, 'fillOpacity': 0.1}
            ).add_to(m)
        except Exception as e:
            print(f"Não foi possível obter o contorno para '{cidade_contexto}': {e}")


    for idx, row in gdf.iterrows():
        codigo = row['codigo']
        tipo = row['tipo']
        
        cor = ''
        if codigo in ids_estacoes_filtradas:
            cor = 'red' if tipo == 'Fluviometrica' else 'blue'
        elif mostrar_todas:
            cor = 'pink' if tipo == 'Fluviometrica' else 'lightblue'
        else:
            continue

        popup_html = f"""
        <b>Estação:</b> {codigo}<br>
        <b>Tipo:</b> {tipo}<br>
        <button onclick="navigator.clipboard.writeText('{codigo}').then(() => alert('Código {codigo} copiado!'))" style="cursor: pointer; border: 1px solid #ccc; border-radius: 3px; margin-top: 5px;">
            Copiar Código
        </button>
        """
        popup = folium.Popup(popup_html, max_width=200)

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup,
            tooltip=f"Estação: {codigo}",
            icon=folium.Icon(color=cor, icon='info-sign')
        ).add_to(m)

    folium.LayerControl().add_to(m)
    
    m.save(output_path)
    print(f"Mapa gerado com sucesso: {output_path}")