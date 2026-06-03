import os
import re
import pandas as pd

def parse_ris_to_excel(input_filepath, output_filepath):
    articles = []
    registro_articulos = {}
    list_keys = ['AU', 'KW'] # Columnas que pueden tener varias entradas.

    with open(input_filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line: # Si no se detecta una línea con contenido se continua.
                continue

            match = re.match(r"^([A-Z0-9]{2})\s*-\s*(.*)$", line) # Detecta dos letras seguidas de un guión y el valor.
            if not match:
                continue

            key, value = match.groups()
            key = key.strip()
            value = value.strip()

            if key == 'TY': # Inicia registro
                if registro_articulos:
                    for k, v in registro_articulos.items():
                        if isinstance(v, list):
                            registro_articulos[k] = "; ".join(v)
                    articles.append(registro_articulos)
                registro_articulos = {'TY': value}
            
            elif key == 'ER': # Termina registro
                for k, v in registro_articulos.items():
                    if isinstance(v, list):
                        registro_articulos[k] = "; ".join(v)
                articles.append(registro_articulos)
                registro_articulos = {}
            
            elif key in list_keys: # Multiples valores para una clave
                if key not in registro_articulos:
                    registro_articulos[key] = []
                registro_articulos[key].append(value)
            
            else: # Un solo valor para una clave
                registro_articulos[key] = value 

    df = pd.DataFrame(articles) # Conversión a DataFrame 
    df.to_excel(output_filepath, index=False) # Exportación a archivo .xlsx
    
    print(f"Procesamiento exitoso. {len(articles)} artículos exportados a {output_filepath}")
    return df

if __name__ == "__main__":

    ruta_entrada = input("Ingresa el nombre del archivo RIS: ")
    if not ruta_entrada.lower().endswith('.ris'): # Si no termina en la extensión para RIS entonces se le agrega.
        ruta_entrada += '.ris'

    ruta_salida= input("Ingresa el nombre del archivo Excel que almacenará los artículos: ")
    if not ruta_salida.lower().endswith('.xlsx'): # Si no termina en la extensión para Excel entonces se le agrega.
        ruta_salida += '.xlsx'

    if not os.path.exists(ruta_entrada):
        print(f"Error: No se pudo encontrar el archivo '{ruta_entrada}'.")
        print("Verifica que el nombre sea correcto y que esté en el directorio adecuado.")
    else:
        print(f"Archivo detectado. Iniciando la conversión de '{ruta_entrada}'...")
        
        dataframe_final = parse_ris_to_excel(ruta_entrada, ruta_salida)
        
        print("Proceso finalizado. Puedes revisar tu Excel en el explorador de archivos.")
