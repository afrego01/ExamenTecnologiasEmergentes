#ALBERTO DANIEL FREGOSO ESQUEDA  20310168

import requests
import hashlib
import time
import pandas as pd # type: ignore
import sqlite3

url = 'https://restcountries.com/v3.1/all'

respuesta = requests.get(url)
paises = respuesta.json()

datos = []

for pais in paises:
    inicio_tiempo = time.time()
    
    region = pais.get('region', 'Desconocida')
    
    idiomas = pais.get('languages', {})
    if idiomas:
        idioma = list(idiomas.values())[0]
    else:
        idioma = 'Desconocido'
    
    sha1_idioma = hashlib.sha1(idioma.encode()).hexdigest()
    
    tiempo_transcurrido = time.time() - inicio_tiempo
    
    datos.append({
        'Región': region,
        'País': pais.get('name', {}).get('common', 'Desconocido'),
        'Idioma': idioma,
        'SHA1 Idioma': sha1_idioma,
        'Tiempo': tiempo_transcurrido
    })

df = pd.DataFrame(datos)

print("Tiempo total:", df['Tiempo'].sum())
print("Tiempo promedio:", df['Tiempo'].mean())
print("Tiempo mínimo:", df['Tiempo'].min())
print("Tiempo máximo:", df['Tiempo'].max())

conexion = sqlite3.connect('paises.db')
df.to_sql('paises', conexion, if_exists='replace', index=False)
conexion.close()

df.to_json('datos.json', orient='records')
