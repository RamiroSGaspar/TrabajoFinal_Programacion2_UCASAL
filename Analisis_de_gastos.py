'''
Universidad Católica de Salta
Programación 2 - 2ndo Semestre
TP4
autor: Gaspar Ramiro Sebastian

Trabajo Final:
Programa: Analisis de Gastos
'''

import numpy as np
import matplotlib.pyplot as plt
import csv
import calendar
import os
import shutil
from datetime import datetime

def analisis_csv():
    # Listas para recolectar datos del .csv
    gastos = []
    meses = []
    años = []
    categorias = []
    dias = [] # nueva lista
    descripciones = [] # nueva lista
    
    with open('GastosMensuales.csv','r') as archivo:
        lector = csv.DictReader(archivo)
        
        for fila in lector:
            gastos.append(float(fila['precio'].strip()))
            dias.append(int(fila['dia'].strip())) # ahora se recibe el dia de los gastos
            meses.append(int(fila['mes'].strip()))
            años.append(int(fila['año'].strip()))
            categorias.append(fila['categoria'].strip().lower()) 
            descripciones.append(fila['descripcion'].strip().lower()) # Se agrego la columna descripcion
    
    return gastos,dias,meses,años,categorias,descripciones

'''
Nota: Se hizo una corrección respecto a el ej 14 del tp anterior, donde
se podia malinterpetrar la eleccion de mensual y anual, donde no se aclara que mensual
era el gasto de todos los meses en el año y no en un mes, lo mismo pasaba con anual.
Ahora se simplifico con año y años, ademas de agregar mes. Se hizo este cambio en
todas las funciones que grafican.
'''

# Funciones de apoyo para las funciones que grafican (adicion nueva)
def pedir_año_para_grafico(año_min=1900, año_max=2100):
    while True:
        x = input("Ingresa el año: ").strip() # Se ingresa primero en str para aplicar la funcion len()
        if len(x) != 4 or not x.isdigit(): # Se verifica si cumple con el formato y si contiene digitos
            print("Error: el año debe tener formato 0000 (4 dígitos).")
            continue

        # Se convierte y se verifica el rango
        try: año = int(x)
        except ValueError:
            print("Error: el año no es un número válido.")
            continue

        if año_min <= año <= año_max: return año
        else: print(f"Error: el año debe estar entre {año_min} y {año_max}.")
        
def pedir_mes_para_grafico():
    while True:
        try:
            mes = int(input("Ingresa el mes: "))
            if mes >= 1 and mes <= 12:
                return mes
            else: print("Error: el mes debe ser valido")
        except ValueError: print("Error: ingreso no valido")

# Funciones Graficas
def grafico_gastos_generales_plot(gastos,meses,años,dias):
    '''
    permite graficar los gastos generales
    el usuario elige si quiere ver los gastos por mes, año o años
    retorna el grafico segun la eleccion del usuario
    '''
    datos = {} # Diccionario para el manejo de valores para graficar
    
    try: 
        desicion = input("¿Que gastos quieres ver en el gráfico? (opciones: 'mes','año' o 'años'):  ").strip().lower()
        if desicion == "año":
            print("Ingresa el año donde quieres ver los gastos mensaules (Formato: 0000): ")
            año_filtro = pedir_año_para_grafico()
            
            for g, m, a in zip(gastos,meses,años): # Se emparejan en una tupla los valores mediante zip() y se recorren
                if a == año_filtro:
                    if m not in datos: datos[m] = g # Se agrega dentro de el diccionario la clave m (el numero del mes) y se le da como valor el gasto
                    else: datos[m] += g # Se acumula el gasto dentro de una clave ya existente
            
            if len(datos.values()) <= 1:
                print(f"\nMENSAJE: El {año_filtro} no tiene los suficientes datos para graficar")
            
            # grafica opcion: año
            elif datos:
                plt.title(f"GRAFICO ANUAL: {año_filtro} - Grafico Plot")
                datos_ordenados = dict(sorted(datos.items())) # se ordena para mostrar la linea continua
                
                plt.plot(datos_ordenados.keys(), datos_ordenados.values())
                plt.scatter(datos_ordenados.keys(), datos_ordenados.values())
                
                # Para el eje x se muestan los meses exactos, convirtiendo las claves en una lista.
                # Despues se crea una lista comprimida que genera los nombres de los meses con ayuda
                # de el diccionario nombre_meses:
                plt.xticks(list(datos_ordenados.keys()), [nombres_meses[m] for m in datos_ordenados.keys()]) 
                
                plt.yticks(list(datos_ordenados.values()))
                plt.grid(True, alpha=0.3)
                plt.xlabel("Mes")
                plt.ylabel("Gastos")
                plt.show()

        elif desicion == "años": 
            for g, m, a in zip(gastos,meses,años):
                if a not in datos: datos[a] = g
                else: datos[a] += g
            
            if len(datos.values()) <= 1:
                print(f"\nMENSAJE: No tiene los suficientes datos para graficar")
            
            # grafica opcion: años
            elif datos:
                datos_ordenados = dict(sorted(datos.items())) # se ordena datos por año
                plt.title("GRAFICO POR AÑOS - Grafico Plot")
                plt.plot(datos_ordenados.keys(), datos_ordenados.values())
                plt.scatter(datos_ordenados.keys(), datos_ordenados.values())
                plt.xticks(list(datos_ordenados.keys()))
                plt.yticks(list(datos_ordenados.values()))
                plt.grid(True, alpha=0.3)
                plt.xlabel("Año")
                plt.ylabel("Gastos")
                plt.show()
        
        # adicion: grafico plot nuevo, muestra los gastos de un mes en especifico, en un año especifico
        elif desicion == "mes":
            print("Ingresa el año donde quieres ver los gastos mensuales (Formato: 0000)")
            año_filtro = pedir_año_para_grafico()
            print("Ingresa el mes donde quieres ver los gastos por mes (1-12): ")
            mes_filtro = pedir_mes_para_grafico()
            
            for g, m, a, d in zip(gastos,meses,años,dias):
                if a == año_filtro and m == mes_filtro:
                    if d not in datos: datos[d] = g
                    else: datos[d] += g
            
            if len(datos.values()) <= 1:
                print(f"\nMENSAJE: El mes {mes_filtro} del {año_filtro} no tiene los suficientes datos para graficar")
            
            # grafica opcion: mes     
            elif datos:
                datos_ordenados = dict(sorted(datos.items())) # se ordena datos por dia
                plt.title(f"GRAFICO DEL MES: {mes_filtro}/{año_filtro} - Grafico Plot")
                plt.plot(datos_ordenados.keys(), datos_ordenados.values())
                plt.scatter(datos_ordenados.keys(), datos_ordenados.values())
                plt.xticks(list(datos_ordenados.keys()))
                plt.yticks(list(datos_ordenados.values()))
                plt.grid(True, alpha=0.3)
                plt.xlabel("Dia")
                plt.ylabel("Gastos")
                plt.show()
        
        else: print("Error. Se ingreso una palabra no valido, vuelve a intentar")
    
    except ValueError: print("Error: Se ingreso un dato invalido, vuelve a intentar")

def grafico_gastos_generales_barra(gastos,meses,años,dias):
    '''
    permite graficar los gastos generales
    el usuario elige si quiere ver los gastos por mes, año o años
    retorna el grafico segun la eleccion del usuario
    '''
    datos = {}
    
    try:
        desicion = input("¿Que gastos quieres ver en el gráfico? (opciones: 'mes','año' o 'años'):  ").strip().lower()
        if desicion == "año":
            print("Ingresa el año donde quieres ver los gastos mensuales (Formato: 0000)")
            año_filtro = pedir_año_para_grafico()
            
            for g,m,a in zip(gastos,meses,años):
                if a == año_filtro:
                    if m not in datos: datos[m] = g
                    else: datos[m] += g
            
            if len(datos.values()) <= 1:
                print(f"\nMENSAJE: El {año_filtro} no tiene los suficientes datos para graficar")
            
            elif datos:
                datos_ordenados = dict(sorted(datos.items()))
                plt.title(f"GRAFICO ANUAL: {año_filtro} - Grafico de Barras")
                plt.bar(datos_ordenados.keys(), datos_ordenados.values())
                plt.xticks(list(datos_ordenados.keys()), [nombres_meses[m] for m in datos_ordenados.keys()])
                plt.yticks(list(datos_ordenados.values()))
                plt.grid(True, alpha=0.3)
                plt.xlabel("Mes")
                plt.ylabel("Gastos")
                plt.show()
        
        elif desicion == "años":
            for g,m,a in zip(gastos,meses,años):
                if a not in datos: datos[a] = g
                else: datos[a] += g
            
            if len(datos.values()) <= 1:
                print(f"\nMENSAJE: no tiene los suficientes datos para graficar")
            
            elif datos:
                datos_ordenados = dict(sorted(datos.items()))
                plt.title("GRAFICO POR AÑOS - Grafico de Barras")
                plt.bar(datos_ordenados.keys(), datos_ordenados.values())
                plt.xticks(list(datos_ordenados.keys()))
                plt.yticks(list(datos_ordenados.values()))
                plt.grid(True, alpha=0.3)
                plt.xlabel("Año")
                plt.ylabel("Gastos")
                plt.show()
        
        elif desicion == "mes":
            print("Ingresa el año donde quieres ver los gastos mensuales (Formato: 0000)")
            año_filtro = pedir_año_para_grafico()
            print("Ingresa el mes donde quieres ver los gastos por mes (1-12): ")
            mes_filtro = pedir_mes_para_grafico()

            for g,m,a,d in zip(gastos,meses,años,dias):
                if a == año_filtro and m == mes_filtro:
                    if d not in datos: datos[d] = g
                    else: datos[d] += g
            
            if len(datos.values()) <= 1:
                print(f"\nMENSAJE: El mes {mes_filtro} del {año_filtro} no tiene los suficientes datos para graficar")
            
            elif datos:
                datos_ordenados = dict(sorted(datos.items()))
                plt.title(f"GRAFICO DEL MES: {mes_filtro}/{año_filtro} - Grafico de Barras") 
                plt.bar(datos_ordenados.keys(), datos_ordenados.values())
                plt.xticks(list(datos_ordenados.keys()))
                plt.yticks(list(datos_ordenados.values()))
                plt.grid(True, alpha=0.3)
                plt.xlabel("Dia")
                plt.ylabel("Gastos")
                plt.show()
            
        else: print("Error. Se ingreso una palabra no valido, vuelve a intentar")
        
    except ValueError: print("Error: Se ingreso un dato no valido, vuelve a intentar")
    
def grafico_gastos_por_categoria(gastos, meses, años, categorias, dias):
    '''
    permite graficar los gastos por categoria
    el usuario elige si quiere ver los gastos por mes, año o años
    retorna el grafico segun la eleccion del usuario
    '''
    datos = {}
    
    try:
        desicion = input("¿Que gastos quieres ver en el gráfico? (opciones: 'mes','año' o 'años'):  ").strip().lower()
        if desicion == "año":
            print("Ingresa el año donde quieres ver los gastos por categoría (Formato: 0000): ")
            año_filtro = pedir_año_para_grafico()
            
            for g, m, a, c in zip(gastos, meses, años, categorias):
                if a == año_filtro:
                    if c not in datos: datos[c] = g
                    else: datos[c] += g
                    
            if len(datos.values()) <= 1:
                print(f"\nMENSAJE: El {año_filtro} no tiene los suficientes datos para graficar")
            
            elif datos:
                plt.title(f"GASTOS POR CATEGORÍA - Año {año_filtro} - Gráfico de Barras")
                plt.bar(datos.keys(), datos.values())
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3)
                plt.xlabel("Categorías")
                plt.ylabel("Total Gastado")
                plt.tight_layout()
                plt.show()
                
        elif desicion == "años":
            # Se encuentra el rango de años para mostrarlo en el título
            año_min = min(años)
            año_max = max(años)
            
            for g, m, a, c in zip(gastos, meses, años, categorias):
                if c not in datos: datos[c] = g
                else: datos[c] += g
            
            if len(datos.values()) <= 1:
                print(f"\nMENSAJE: no tiene los suficientes datos para graficar")
            
            elif datos:
                if año_min == año_max:
                    plt.title(f"GASTOS POR CATEGORÍA - Año {año_min} - Gráfico de Barras")
                else:
                    plt.title(f"GASTOS POR CATEGORÍA - Período {año_min}-{año_max} - Gráfico de Barras")
                
                plt.bar(datos.keys(), datos.values())
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3)
                plt.xlabel("Categorías")
                plt.ylabel("Total Gastado")
                plt.tight_layout()
                plt.show()
        
        elif desicion == "mes":
            print("Ingresa el año donde quieres ver los gastos por categoría (Formato: 0000): ")
            año_filtro = pedir_año_para_grafico()
            print("Ingresa el mes donde quieres ver los gastos por categoria (1-12): ")
            mes_filtro = pedir_mes_para_grafico()
            
            for g, m, a, d, c in zip(gastos, meses, años, dias,categorias):
                if a == año_filtro and m == mes_filtro:
                    if c not in datos: datos[c] = g
                    else: datos[c]+= g
            
            if len(datos.values()) <= 1:
                    print(f"\nMENSAJE: El mes {mes_filtro} del {año_filtro} no tiene los suficientes datos para graficar")
                
            elif datos:
                plt.title(f"GASTOS POR CATEGORÍA - Mes {mes_filtro}/{año_filtro} - Gráfico de Barras")
                plt.bar(datos.keys(), datos.values())
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3)
                plt.xlabel("Categorías")
                plt.ylabel("Total Gastado")
                plt.tight_layout()
                plt.show()
        
        else: print("Error. Se ingresó una palabra no válida, vuelve a intentar")
            
    except ValueError: print("Error: Se ingresó un dato no válido, vuelve a intentar")


# Funciones de Calculo
def calculos_generales(gastos,meses,años):
    '''
    permite realizar calculos generales sobre todos los gastos
    el usuario elige el tipo de calculo
    retorna los resultados segun la eleccion del usuario
    '''
    lista_gastos = []
    
    print("--CALCULOS GENERALES--")
    desicion = input("¿Quieres realizar los calculos de forma 'mensual' o 'anual'? ").strip().lower()
    
    try: 
        if desicion == "mensual":
            print("\n--CALCULOS GENERALES (de forma mensual)--")
            año_filtro = int(input("Ingresa el año donde quieres ver los gastos mensaules (Formato: 0000): "))
            
            # Creacion del array, que solo sigue los meses dentro de un solo año    
            for g,m,a in zip(gastos,meses,años):
                if a == año_filtro:
                    lista_gastos.append(g)
        
            array_gastos = np.array(lista_gastos)
            
            print("\n¿Qué quieres revisar?")
            print("- Ingresa 'total' para ver el total de gastos")
            print("- Ingresa 'promedio' para ver el resultado")
            print("- Ingresa 'maximo' para ver el gasto maximo")
            print("- Ingresa 'minimo' para ver el gasto minimo")
            print("- Ingresa 'todo' para ver todas las opciones")
            
            desicion_2 = input("Ingresa la opcion: ").strip().lower()
            
            if desicion_2 == "total": print("\nEl total de los gastos: ",np.sum(array_gastos))
            elif desicion_2 == "promedio": print("\nEl promedio de los gastos: ", np.average(array_gastos))
            elif desicion_2 == "maximo": print("\nEl gasto maximo es: ",np.max(array_gastos))
            elif desicion_2 == "minimo": print("\nEl gasto minimo es: ",np.min(array_gastos))
            elif desicion_2 == "todo":
                print("\n--Todos los calculos--")
                print("El total de los gastos: ",np.sum(array_gastos))
                print("El promedio de los gastos: ", np.average(array_gastos))
                print("El gasto maximo es: ",np.max(array_gastos))
                print("El gasto minimo es: ",np.min(array_gastos))
            
        elif desicion == "anual":
            print("\n--CALCULOS GENERALES (de forma anual)--")
            for g,m,a in zip(gastos,meses,años):
                lista_gastos.append(g)
        
            array_gastos = np.array(lista_gastos)
            
            print("\n¿Qué quieres revisar?")
            print("- Ingresa 'total' para ver el total de gastos")
            print("- Ingresa 'promedio' para ver el resultado")
            print("- Ingresa 'maximo' para ver el gasto maximo")
            print("- Ingresa 'minimo' para ver el gasto minimo")
            print("- Ingresa 'todo' para ver todas las opciones")
            
            desicion_2 = input("Ingresa la opcion: ").strip().lower()
            
            if desicion_2 == "total": print("\nEl total de los gastos: ",np.sum(array_gastos))
            elif desicion_2 == "promedio": print("\nEl promedio de los gastos: ", np.average(array_gastos))
            elif desicion_2 == "maximo": print("\nEl gasto maximo es: ",np.max(array_gastos))
            elif desicion_2 == "minimo": print("\nEl gasto minimo es: ",np.min(array_gastos))
            elif desicion_2 == "todo":
                print("\n--Todos los calculos--")
                print("El total de los gastos: ",np.sum(array_gastos))
                print("El promedio de los gastos: ", np.average(array_gastos))
                print("El gasto maximo es: ",np.max(array_gastos))
                print("El gasto minimo es: ",np.min(array_gastos))
            else: print("Error. Ingreso no valido")
        else: print("Error: Se ingreso una palabra no valida, vuelve a intentar") 
        
    except ValueError: print("Error: Se ingreso un dato no valido, vuelve a intentar")

def calculos_especificos(gastos,meses,años,categorias):
    '''
    permite realizar calculos especificos por categoria
    el usuario elige la categoria y el tipo de calculo
    retorna los resultados segun la eleccion del usuario
    '''
    diccionario = {}
    
    print("\n--CALCULOS ESPECIFICOS--")
    desicion = input("¿Quieres realizar los calculos de forma 'mensual' o 'anual'? ").strip().lower()
    
    try:
        if desicion == "mensual":
            print("\n--CALCULOS POR CATEGORIA (de forma mensual)--")
            año_filtro = int(input("Ingresa el año donde quieres ver los gastos mensaules (Formato: 0000): "))
            
            for g,m,a,c in zip(gastos,meses,años,categorias):
                if a == año_filtro:
                    if c not in diccionario: 
                        diccionario[c] = []
                    diccionario[c].append(g)
            
            print("\nEstas son las categorias disponibles: ")
            for elemento in diccionario.keys():
                print(f"- '{elemento}', ingresa esa palbra para revisar las opciones de calculo")
            
            desicion_2 = input("Ingresa la categoria: ").strip().lower()
            if desicion_2 in diccionario:
                
                array_gastos = np.array(diccionario[desicion_2])
            
                print("\n¿Qué quieres revisar?")
                print("- Ingresa 'total' para ver el total de gastos por categoria")
                print("- Ingresa 'promedio' para ver el promedio de gastos por categoria")
                print("- Ingresa 'maximo' para ver el gasto maximo por categoria")
                print("- Ingresa 'minimo' para ver el gasto minimo por categoria")
                print("- Ingresa 'todo' para ver todas las opciones")
                
                desicion_3 = input("Ingresa la opcion: ").strip().lower()
                
                if desicion_3 == "total":print(f"\nEl total de la categoria '{desicion_2}': ",np.sum(array_gastos))
                elif desicion_3 == "promedio": print(f"\nEl promedio de la categoria '{desicion_2}': ",np.average(array_gastos))
                elif desicion_3 == "maximo": print(f"\nEl gasto maximo de la categoria '{desicion_2}': ",np.max(array_gastos))
                elif desicion_3 == "minimo": print(f"\nEl gasto minimo de la categoria '{desicion_2}': ",np.min(array_gastos))
                elif desicion_3 == "todo":
                    print(f"\n--Todos los calculos sobre {desicion_2}--")
                    print(f"El promedio de la categoria '{desicion_2}': ",np.average(array_gastos))
                    print(f"El gasto maximo de la categoria '{desicion_2}': ",np.max(array_gastos))
                    print(f"El gasto minimo de la categoria '{desicion_2}': ",np.min(array_gastos))
                else: print("Error. Ingreso no valido")
                    
            else: print("Error. No se encontro la categoria")

        elif desicion == "anual":
            print("\n--CALCULOS POR CATEGORIA (de forma anual)--")
            
            for g,m,a,c in zip(gastos,meses,años,categorias):
                if c not in diccionario: 
                    diccionario[c] = []
                diccionario[c].append(g)
            
            print("\nEstas son las categorias disponibles: ")
            for elemento in diccionario.keys():
                print(f"- '{elemento}', ingresa esa palbra para revisar las opciones de calculo")
            
            desicion_2 = input("Ingresa la categoria: ").strip().lower()
            if desicion_2 in diccionario:
                
                array_gastos = np.array(diccionario[desicion_2])
            
                print("\n¿Qué quieres revisar?")
                print("- Ingresa 'total' para ver el total de gastos por categoria")
                print("- Ingresa 'promedio' para ver el promedio de gastos por categoria")
                print("- Ingresa 'maximo' para ver el gasto maximo por categoria")
                print("- Ingresa 'minimo' para ver el gasto minimo por categoria")
                print("- Ingresa 'todo' para ver todas las opciones")
            
                desicion_3 = input("Ingresa la opcion: ").strip().lower()
                
                if desicion_3 == "total":print(f"\nEl total de la categoria '{desicion_2}': ",np.sum(array_gastos))
                elif desicion_3 == "promedio": print(f"\nEl promedio de la categoria '{desicion_2}': ",np.average(array_gastos))
                elif desicion_3 == "maximo": print(f"\nEl gasto maximo de la categoria '{desicion_2}': ",np.max(array_gastos))
                elif desicion_3 == "minimo": print(f"\nEl gasto minimo de la categoria '{desicion_2}': ",np.min(array_gastos))
                elif desicion_3 == "todo":
                    print(f"\n--Todos los calculos sobre {desicion_2}--")
                    print(f"El promedio de la categoria '{desicion_2}': ",np.average(array_gastos))
                    print(f"El gasto maximo de la categoria '{desicion_2}': ",np.max(array_gastos))
                    print(f"El gasto minimo de la categoria '{desicion_2}': ",np.min(array_gastos))
                else: print("Error. Ingreso no valido")
            
            else: print("Error. No se encontro la categoria")   
        else: print("Error. Se ingreso una palabra no valida, vuelve a intentar")
        
    except ValueError: print("Error: Se ingreso un dato no valido, vuelve a intentar")


# CRUD
def guardar_csv(gastos, dias, meses, años, categorias, descripciones, archivo="GastosMensuales.csv"):
    '''
    permite guardar los datos en el archivo .csv
    crea un backup del archivo original antes de guardar los cambios
    retorna True si se guardo exitosamente, False en caso de error
    '''
    try:
        # se crea un backup antes de guardar
        if os.path.exists(archivo):  # verifica si el archivo existe
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # genera timestamp: 20251022_143025
            backup = f"{archivo}.backup_{timestamp}"  # nombre: GastosMensuales.csv.backup_20251022_143025
            shutil.copy2(archivo, backup)  # copia el archivo con el nuevo nombre (incluye metadatos)
            print(f"- Backup creado: {backup}")  # muestra confirmación
        
        # verificacion para confirmar la misma longitud de elementos
        if not (len(gastos) == len(dias) == len(meses) == len(años) == len(categorias) == len(descripciones)):
            print("Error: Las listas de datos tienen longitudes diferentes")
            return False
        
        # se abre el archivo en modo escritura
        with open(archivo, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['año', 'mes', 'dia', 'categoria', 'precio', 'descripcion'])
            
            # se recorre respetando el formato de fecha consistente con 2 dígitos
            for i in range(len(gastos)):
                writer.writerow([
                    años[i],
                    str(meses[i]).zfill(2),   # 5 → "05"
                    str(dias[i]).zfill(2),    # 7 → "07"
                    categorias[i],
                    gastos[i],
                    descripciones[i]
                ])
        
        print(f"+ Datos guardados exitosamente en '{archivo}'")
        print(f"+ Total de registros guardados: {len(gastos)}")
        return True
        
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        return False

def agregar_gasto(gastos, dias, meses, años, categorias, descripciones):
    '''
    permite agregar un nuevo gasto al sistema
    '''
    # Se guardan datos que pueden cambiar en el tiempo
    año_actual = datetime.now().year
    print("\n--Agregar un nuevo gasto--")
    
    # VALIDACIÓN DEL AÑO
    while True:
        try:
            año = int(input("Ingresa el año del gasto (ej: 2025): "))
            if año < 2000 or año > año_actual:
                print(f"Año invalido. Por favor ingrese un año entre 2000 y {año_actual}")
                continue
            break
        except ValueError: 
            print("Error: ingreso no valido.")
    
    # VALIDACIÓN DEL MES
    while True:
        try:
            mes = int(input("Ingresa el mes (1-12): "))
            if mes < 1 or mes > 12:
                print("Mes inválido. Por favor ingrese un mes entre 1 y 12")
                continue
            break
        except ValueError: 
            print("Error: Por favor ingresa un número válido.")
        
    # VALIDACIÓN DEL DIA
    while True:
        try:
            dia = int(input("Ingresa el numero del dia del gasto: "))
            num_dias_mes = calendar.monthrange(año, mes)[1]
            
            if dia > num_dias_mes or dia < 1:
                print(f"Dia invalido. Este mes tiene {num_dias_mes} días")
                continue
            break
        except ValueError: 
            print("Error: ingreso no valido")
        
    # VALIDACIÓN DE LA CATEGORIA
    print("\nCategorias Existentes: ")
    categorias_unicas = list(set(categorias))
    categorias_unicas.sort()
    
    # se muestran las categorias existentes:
    for i, cat in enumerate(categorias_unicas, 1):
        print(f"{i}. {cat}")
        
    opcion_nueva = len(categorias_unicas) + 1
    print(f"{opcion_nueva}. Crear nueva categoría")
    
    while True:
        try:
            opcion = int(input("\nElige una opción: "))
                
            # se verifica que la opción sea válida
            if opcion < 1 or opcion > opcion_nueva:
                print(f"Por favor elige una opción entre 1 y {opcion_nueva}")
                continue
            
            # opcion de categoria existente
            if opcion <= len(categorias_unicas):
                categoria_elegida = categorias_unicas[opcion - 1]
                
            # opcion de crear una nueva categoria
            else:
                categoria_elegida = input("Nombre de la nueva categoría: ").strip().lower()
                while categoria_elegida == "":
                    print("La categoría no puede estar vacía")
                    categoria_elegida = input("Nombre de la nueva categoría: ").strip().lower()
            
            break
        except ValueError: 
            print("Error: ingreso no valido")

    # VALIDACION DEL PRECIO
    while True:
        try:
            precio = float(input("\nIngresa el precio del gasto: $"))
            if precio <= 0: 
                print("El precio debe ser mayor que 0")
                continue
            break
        except ValueError: 
            print("Error: ingreso no valido")
        
    # VALIDACION DE LA DESCRIPCION (OPCIONAL)
    print("\n¿Deseas agregar una descripción?")
    descripcion = input("Descripcion (presiona enter para omitir): ").strip()
    
    if descripcion == "": 
        descripcion = "-"
    
    # Agregado a las listas
    años.append(año)
    meses.append(mes)
    dias.append(dia)
    categorias.append(categoria_elegida)
    gastos.append(precio)
    descripciones.append(descripcion)
    
    print(f"\nGasto agregado exitosamente:")
    print(f"- Fecha: {dia:02d}/{mes:02d}/{año}")
    print(f"- Categoría: {categoria_elegida}")
    print(f"- Precio: ${precio:.2f}")
    if descripcion != "-":
        print(f"- Descripción: {descripcion}")

def menu_agregar_gastos(gastos, dias, meses, años, categorias, descripciones):
    '''
    permite agregar varios gastos seguidos
    al finalizar, se pregunta si se quieren guardar los cambios
    en caso de no guardar, se pide confirmacion clara
    ''' 
    gastos_agregados = 0
    
    while True:
        # se llama a la función que agrega UN gasto
        agregar_gasto(gastos, dias, meses, años, categorias, descripciones)
        gastos_agregados += 1
        
        print("\n" + "="*40)
        continuar = input("¿Quieres agregar otro gasto? (s/n): ").lower().strip()
        
        if continuar != 's':
            break
    
    print(f"\nSe agregaron {gastos_agregados} gasto(s) en total")
    
    # confirmacion clara al no guardar
    respuesta = input("¿Quieres guardar los cambios en el archivo? (s/n): ").lower().strip()
    
    if respuesta == 's': 
        guardar_csv(gastos, dias, meses, años, categorias, descripciones)
    else:
        print("\nADVERTENCIA: Los gastos agregados NO se guardarán en el archivo")
        confirmar = input("¿Estás seguro de NO guardar? (s/n): ").lower().strip()
        if confirmar != 's':
            print("\nGuardando cambios...")
            guardar_csv(gastos, dias, meses, años, categorias, descripciones)
        else:
            print("- Cambios descartados")

def eliminar_gasto(gastos, dias, meses, años, categorias, descripciones):
    '''
    permite eliminar un gasto existente
    el usuario selecciona el gasto por numero
    se pide confirmacion antes de eliminar
    '''
    if len(gastos) == 0:
        print("\nNo hay gastos para eliminar")
        return
    
    ver_gastos(gastos, dias, meses, años, categorias, descripciones)
    
    try:
        num = int(input("\n¿Qué gasto deseas eliminar? (número o 0 para cancelar): "))
        
        if num == 0:
            print("Operación cancelada")
            return
            
        if num < 1 or num > len(gastos):
            print("Número inválido")
            return
        
        idx = num - 1
        
        print(f"\n¿Eliminar este gasto?")
        print(f"- Fecha: {dias[idx]:02d}/{meses[idx]:02d}/{años[idx]}")
        print(f"- Categoría: {categorias[idx]}")
        print(f"- Precio: ${gastos[idx]:.2f}")
        print(f"- Descripción: {descripciones[idx]}")
        
        confirmar = input("\nConfirmar eliminación (s/n): ").lower().strip()
        
        if confirmar == 's':
            # eliminar de todas las listas
            del gastos[idx]
            del dias[idx]
            del meses[idx]
            del años[idx]
            del categorias[idx]
            del descripciones[idx]
            
            print("- Gasto eliminado correctamente")
            
            # se pregunta para guardar
            guardar = input("¿Guardar cambios en archivo? (s/n): ").lower().strip()
            if guardar == 's': guardar_csv(gastos, dias, meses, años, categorias, descripciones)
                
        else: print("Operación cancelada")
            
    except ValueError: print("Error: Entrada inválida")

def ver_gastos(gastos, dias, meses, años, categorias, descripciones):
    '''
    permite ver todos los gastos registrados en el sistema
    muestra la fecha, categoria, precio y descripcion de cada gasto
    ademas muestra el total de gastos y la suma total de los mismos
    '''
    if len(gastos) == 0:
        print("\nNo hay gastos registrados")
        return
    
    print("\n--GASTOS REGISTRADOS--")
    for i in range(len(gastos)):
        print(f"{i+1}. {dias[i]:02d}/{meses[i]:02d}/{años[i]} - {categorias[i]} - ${gastos[i]:.2f} - {descripciones[i]}")
    
    print(f"\nTotal: {len(gastos)} gastos | ${sum(gastos):.2f}")

def modificar_gasto(gastos, dias, meses, años, categorias, descripciones):
    """
    Permite modificar un gasto existente.
    El usuario selecciona el gasto por número y puede cambiar cualquier campo.
    Presionando ENTER mantiene el valor actual.
    """
    
    # se verifica que hay gastos para modificar
    if len(gastos) == 0:
        print("\nNo hay gastos para modificar")
        return
    
    ver_gastos(gastos, dias, meses, años, categorias, descripciones)
    
    try:
        num = int(input("\n¿Qué gasto deseas modificar? (número o 0 para cancelar): "))
        if num == 0:
            print("Operación cancelada")
            return
        if num < 1 or num > len(gastos):
            print("Número inválido")
            return
        
        idx = num - 1  # Se converte a índice (las listas empiezan en 0)
        
        # Se muestrar los datos actuales del gasto seleccionado
        print(f"\n--GASTO ACTUAL--")
        print(f"Fecha: {dias[idx]:02d}/{meses[idx]:02d}/{años[idx]}")
        print(f"Categoría: {categorias[idx]}")
        print(f"Precio: ${gastos[idx]:.2f}")
        print(f"Descripción: {descripciones[idx]}")
        
        print("\n--MODIFICAR GASTO--")
        print("(Presiona ENTER para mantener el valor actual)")
        
        # MODIFICAR AÑO
        año_nuevo = input(f"Nuevo año [{años[idx]}]: ").strip()
        if año_nuevo != "":  # si el usuario ingreso algo
            try:
                año_nuevo = int(año_nuevo)
                año_actual = datetime.now().year
                # validar rango de año
                if año_nuevo < 2000 or año_nuevo > año_actual:
                    print(f"Año inválido. Se mantiene: {años[idx]}")
                    año_nuevo = años[idx]
            except ValueError:
                print("Entrada inválida. Se mantiene el año actual")
                año_nuevo = años[idx]
        else: año_nuevo = años[idx] # si se  presionó ENTER, mantener el valor actual

        
        # MODIFICAR MES
        mes_nuevo = input(f"Nuevo mes (1-12) [{meses[idx]}]: ").strip()
        if mes_nuevo != "":
            try:
                mes_nuevo = int(mes_nuevo)
                if mes_nuevo < 1 or mes_nuevo > 12:
                    print(f"Mes inválido. Se mantiene: {meses[idx]}")
                    mes_nuevo = meses[idx]
            except ValueError:
                print("Entrada inválida. Se mantiene el mes actual")
                mes_nuevo = meses[idx]
        else: mes_nuevo = meses[idx]
        
        # MODIFICAR DÍA
        dia_nuevo = input(f"Nuevo día [{dias[idx]}]: ").strip()
        if dia_nuevo != "":
            try:
                dia_nuevo = int(dia_nuevo)
                # obtener la cantidad de días del mes ingresado
                num_dias_mes = calendar.monthrange(año_nuevo, mes_nuevo)[1]
                # validar que el día sea válido para ese mes
                if dia_nuevo < 1 or dia_nuevo > num_dias_mes:
                    print(f"Día inválido. Se mantiene: {dias[idx]}")
                    dia_nuevo = dias[idx]
            except ValueError:
                print("Entrada inválida. Se mantiene el día actual")
                dia_nuevo = dias[idx]
        else: dia_nuevo = dias[idx]
        
        # MODIFICAR CATEGORÍA
        print("\nCategorías disponibles:")
        # se obtiene las categorias unicas y ordenarlas
        categorias_unicas = sorted(list(set(categorias)))
        # muestra la lista numerada
        for i, cat in enumerate(categorias_unicas, 1):
            print(f"{i}. {cat}")
        print(f"{len(categorias_unicas) + 1}. Crear nueva categoría")
        print(f"{len(categorias_unicas) + 2}. Mantener actual ({categorias[idx]})")
        
        opcion_cat = input("\nElige una opción: ").strip()
        if opcion_cat == "": categoria_nueva = categorias[idx] # si presiono ENTER sin escribir
        else:
            try:
                opcion_cat = int(opcion_cat)
                # si eligio una categoria existente
                if 1 <= opcion_cat <= len(categorias_unicas):
                    categoria_nueva = categorias_unicas[opcion_cat - 1]
                    
                # si eligio crear nueva categoria
                elif opcion_cat == len(categorias_unicas) + 1:
                    categoria_nueva = input("Nombre de la nueva categoría: ").strip().lower()
                    if categoria_nueva == "":
                        print("Categoría vacía. Se mantiene la actual")
                        categoria_nueva = categorias[idx]
                        
                # si eligio mantener actual o cualquier otra opcion
                else: categoria_nueva = categorias[idx]
            except ValueError:
                print("Entrada inválida. Se mantiene la categoría actual")
                categoria_nueva = categorias[idx]
        
        # MODIFICAR PRECIO
        precio_nuevo = input(f"Nuevo precio [${gastos[idx]:.2f}]: $").strip()
        if precio_nuevo != "":
            try:
                precio_nuevo = float(precio_nuevo)
                # validar que sea mayor que 0
                if precio_nuevo <= 0:
                    print("Precio inválido. Se mantiene el precio actual")
                    precio_nuevo = gastos[idx]
            except ValueError:
                print("Entrada inválida. Se mantiene el precio actual")
                precio_nuevo = gastos[idx]
        else:
            precio_nuevo = gastos[idx]
        
        # MODIFICAR DESCRIPCIÓN
        descripcion_nueva = input(f"Nueva descripción [{descripciones[idx]}]: ").strip()
        if descripcion_nueva == "":  # si se resiona ENTER, mantener la actual
            descripcion_nueva = descripciones[idx]
        
        # MOSTRAR RESUMEN DE CAMBIOS
        print("\n--RESUMEN DE CAMBIOS--")
        print(f"Fecha: {dias[idx]:02d}/{meses[idx]:02d}/{años[idx]} -> {dia_nuevo:02d}/{mes_nuevo:02d}/{año_nuevo}")
        print(f"Categoría: {categorias[idx]} -> {categoria_nueva}")
        print(f"Precio: ${gastos[idx]:.2f} -> ${precio_nuevo:.2f}")
        print(f"Descripción: {descripciones[idx]} -> {descripcion_nueva}")
        
        # CONFIRMAR Y APLICAR CAMBIOS
        confirmar = input("\n¿Confirmar cambios? (s/n): ").lower().strip()
        
        if confirmar == 's':
            # se aplican todos los cambios a las listas
            años[idx] = año_nuevo
            meses[idx] = mes_nuevo
            dias[idx] = dia_nuevo
            categorias[idx] = categoria_nueva
            gastos[idx] = precio_nuevo
            descripciones[idx] = descripcion_nueva
            
            print("\n- Gasto modificado exitosamente")
            
            guardar = input("¿Guardar cambios en archivo? (s/n): ").lower().strip()
            if guardar == 's':
                guardar_csv(gastos, dias, meses, años, categorias, descripciones)
        else:
            print("Cambios descartados")
            
    except ValueError:
        print("Error: Entrada inválida")

# diccionario util para graficar 
nombres_meses = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo",
    6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre",
    10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
            
def main():
    gastos, dias, meses, años, categorias, descripciones = analisis_csv()

    while True:
        print("\n" + "="*55)
        print("            SISTEMA DE GESTIÓN DE GASTOS")
        print("="*55)
        print("\n--GRÁFICOS--")
        print("1. Gráfico de gastos por tiempo (plot)")
        print("2. Gráfico de gastos por tiempo (barras)")
        print("3. Gráfico de gastos por categoría")
        
        print("\n--CÁLCULOS--")
        print("4. Cálculos generales")
        print("5. Cálculos por categoría")
        
        print("\n--GESTIÓN DE DATOS--")
        print("6. Ver todos los gastos")
        print("7. Agregar nuevo/s gastos")
        print("8. Modificar un gasto")
        print("9. Eliminar un gasto")
        
        print("\n9. Salir")
        print("="*55)
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "1": grafico_gastos_generales_plot(gastos, meses, años, dias)
        elif opcion == "2": grafico_gastos_generales_barra(gastos, meses, años, dias)
        elif opcion == "3": grafico_gastos_por_categoria(gastos, meses, años, categorias, dias)
        elif opcion == "4": calculos_generales(gastos, meses, años)
        elif opcion == "5": calculos_especificos(gastos, meses, años, categorias)
        elif opcion == "6": ver_gastos(gastos, dias, meses, años, categorias, descripciones)
        elif opcion == "7": menu_agregar_gastos(gastos, dias, meses, años, categorias, descripciones)
        elif opcion == "8": modificar_gasto(gastos, dias, meses, años, categorias, descripciones)
        elif opcion == "9": eliminar_gasto(gastos, dias, meses, años, categorias, descripciones)
        elif opcion == "10":
            print("\nSaliendo del programa...")
            break
        else:
            print("Error. opcion no valida, por favor, intenta de nuevo.")


if __name__ == "__main__":
    main()