import folium
import geopandas
from shapely.geometry import Point
import branca.colormap as cm # Importa a biblioteca para o mapa de cores

def plotar_estacoes(estacoes_filtradas, estacoes_original, mostrar_todas=False, raio_km=0, output_path="html/index.html"):
    if not estacoes_filtradas:
        print("A lista de estações filtradas está vazia. O mapa não pode ser gerado.")
        return
        
    ids_estacoes_filtradas = {item['codigoestacao'] for item in estacoes_filtradas}
    
    dados_plotagem = []
    for item in estacoes_original:
        if item.get("Operando") == "1":
            try:
                dados_plotagem.append({
                    'codigo': item['codigoestacao'],
                    'tipo': item['Tipo_Estacao'],
                    'latitude': float(item['Latitude']),
                    'longitude': float(item['Longitude']),
                    'altitude': float(item.get('Altitude', 0))
                })
            except (ValueError, TypeError, KeyError):
                continue

    if not dados_plotagem:
        print("Nenhuma estação válida para plotar.")
        return

    gdf_total = geopandas.GeoDataFrame(
        dados_plotagem,
        geometry=geopandas.points_from_xy([d['longitude'] for d in dados_plotagem], [d['latitude'] for d in dados_plotagem]),
        crs="EPSG:4326"
    )
    
    gdf_total['altitude'] = gdf_total['altitude'].astype(float)

    gdf_filtradas = gdf_total[gdf_total['codigo'].isin(ids_estacoes_filtradas)].copy()
    gdf_outras = gdf_total[~gdf_total['codigo'].isin(ids_estacoes_filtradas)].copy()
    
    if gdf_filtradas.empty:
        print("Nenhuma das estações filtradas foi encontrada nos dados originais válidos.")
        return

    utm_crs = gdf_filtradas.estimate_utm_crs()
    gdf_filtradas_proj = gdf_filtradas.to_crs(utm_crs)
    gdf_outras_proj = gdf_outras.to_crs(utm_crs)
    distancia_em_metros = raio_km * 1000
    buffers = gdf_filtradas_proj.geometry.buffer(distancia_em_metros)
    area_de_interesse = buffers.unary_union
    indices_proximas = gdf_outras_proj.within(area_de_interesse)
    gdf_proximas = gdf_outras.loc[indices_proximas].copy()
    print(f"Encontradas {len(gdf_proximas)} estações próximas (dentro de um raio de {raio_km} km).")

    map_center = [gdf_filtradas['latitude'].mean(), gdf_filtradas['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=9, tiles="OpenStreetMap")
    
    folium.TileLayer('CartoDB positron', name='Mapa Claro').add_to(m)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Google Satellite').add_to(m)
    
    camada_filtradas_tipo = folium.FeatureGroup(name="Estações Filtradas (por Tipo)", show=True)
    for _, row in gdf_filtradas.iterrows():
        cor = 'red' if row['tipo'] == 'Fluviometrica' else 'blue'
        popup_html = f"<b>Estação:</b> {row['codigo']}<br><b>Tipo:</b> {row['tipo']}"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=f"{row['codigo']} ({row['tipo']})",
            icon=folium.Icon(color=cor, icon='star', prefix='fa')
        ).add_to(camada_filtradas_tipo)
    camada_filtradas_tipo.add_to(m)

    camada_altitude_fluv = folium.FeatureGroup(name="Altitude (Fluviométricas)", show=False) # Começa desligada
    
    gdf_fluv = gdf_filtradas[gdf_filtradas['tipo'] == 'Fluviometrica']
    if not gdf_fluv.empty:
        min_alt, max_alt = gdf_fluv['altitude'].min(), gdf_fluv['altitude'].max()
        
        if min_alt == max_alt:
            max_alt += 1
            
        altitude_steps = [min_alt, min_alt + (max_alt-min_alt)*0.25, min_alt + (max_alt-min_alt)*0.75, max_alt]
        colormap = cm.StepColormap(
            colors=['#007bff', '#28a745', '#ffc107', '#dc3545'], # Azul, Verde, Amarelo, Vermelho
            index=altitude_steps, vmin=min_alt, vmax=max_alt,
            caption="Altitude das Estações Fluviométricas (m)"
        )
        
        for _, row in gdf_fluv.iterrows():
            popup_html = f"<b>Estação:</b> {row['codigo']}<br><b>Altitude:</b> {row['altitude']:.2f} m"
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=7, popup=folium.Popup(popup_html, max_width=200),
                tooltip=f"{row['codigo']} ({row['altitude']:.0f} m)",
                color=colormap(row['altitude']), fill=True,
                fill_color=colormap(row['altitude']), fill_opacity=0.8
            ).add_to(camada_altitude_fluv)
        
        camada_altitude_fluv.add_to(m)
        colormap.add_to(m)

    camada_proximas = folium.FeatureGroup(name=f"Estações no Raio de {raio_km} km", show=mostrar_todas)
    for _, row in gdf_proximas.iterrows():
        cor = 'pink' if row['tipo'] == 'Fluviometrica' else 'lightblue'
        popup_html = f"<b>Estação (Próxima):</b> {row['codigo']}<br><b>Tipo:</b> {row['tipo']}"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=f"Estação: {row['codigo']}",
            icon=folium.Icon(color=cor, icon='info-sign')
        ).add_to(camada_proximas)
    camada_proximas.add_to(m)
    
    folium.LayerControl().add_to(m)
    
    m.save(output_path)
    print(f"Mapa gerado com sucesso: {output_path}")

