import pandas as pd
import googlemaps

# Clave para API Google Maps
gmaps = googlemaps.Client(key='AIzaSyDklP2n2zexmWjeo9CpWBfI174TXzaFftw')

# Lista direcciones
direcciones = [
    'Camino Lo Boza, 120, Pudahuel, Chile',
    'policarpo toro 173, MAIPÚ, Chile',
    'san sebastian 3420, MAIPÚ, Chile',
    'Guadarrama 452, MAIPÚ, Chile',
    'congo belga 3052, MAIPÚ, Chile',
    'gerona 4696, MAIPÚ, Chile',
    'Batalla de Chacabuco 1147, MAIPÚ, Chile',
    'Isabel Riquelme Norte 3142, MAIPÚ, Chile',
    'Carranco 1822, MAIPÚ, Chile',
    'Ingeniero Eduardo Domínguez 549, MAIPÚ, Chile',
    'Pasaje la ñipa sur 208, MAIPÚ, Chile',
    'San martin 3275, MAIPÚ, Chile',
    'dragones de la frontera 3431, MAIPÚ, Chile',
    'Pasaje La Reconquista 2370, MAIPÚ, Chile',
    'Mar de los Sargazos 2382, MAIPÚ, Chile',
    'Av portales 2761, MAIPÚ, Chile',
    'Universidad Cátolica 116, MAIPÚ, Chile',
    'Glaciar Aguila Dos 2592, MAIPÚ, Chile',
    'cerro iglesia 2622, MAIPÚ, Chile',
    'Helecho Sur 18548, Maipú',
    'Abisinia 1367, MAIPÚ, Chile',
    'Avenida Hernán Olguin 397, MAIPÚ, Chile',
    'pelequen 1038, MAIPÚ, Chile',
    'Cardenal Samore 677, MAIPÚ, Chile',
    'Cuatro Alamos 325, MAIPÚ, Chile',
    'garcia hurtado de mendoza 8293, LA FLORIDA, Chile',
    'Colombia 8467, LA FLORIDA, Chile',
    'Colombia 8863, LA FLORIDA, Chile',
    'Santa Aurora 2417 2417, LA FLORIDA, Chile',
    'El Canelo 5925, PEÑALOLÉN, Chile',
    'Los Ombues Sur 8191, PEÑALOLÉN, Chile',
    'Los marroquineros 6115, PEÑALOLÉN, Chile',
    'El bosque 4792, PEÑALOLÉN, Chile',
    'Victoria 4861, PEÑALOLÉN, Chile',
    'Los aymaras 1814, PEÑALOLÉN, Chile',
    'Sendero Jardín Poniente 2595, PEÑALOLÉN, Chile',
    'Rayen 2255, PEÑALOLÉN, Chile',
    'Diagonal Las Torres 2000, PEÑALOLÉN, Chile'
]


# Crea un DataFrame vacío para almacenar las distancias.
df_distancias = pd.DataFrame(index=direcciones, columns=direcciones)

# Calcula las distancias entre cada par de direcciones y guárdalas en el DataFrame.
for origen in direcciones:
    for destino in direcciones:
        if origen != destino:
            resultado = gmaps.distance_matrix(origen, destino)
            distancia = resultado['rows'][0]['elements'][0]['distance']['text']
            df_distancias.at[origen, destino] = distancia

# Guarda el DataFrame en un archivo Excel.
nombre_archivo = 'distancias_santiago.xlsx'
df_distancias.to_excel(nombre_archivo, engine='openpyxl')

print(f"Distancias guardadas en el archivo {nombre_archivo}")
