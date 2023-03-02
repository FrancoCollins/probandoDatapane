import datapane as dp
import pandas as pd

fichero_csv = "DI_U05_A02_PP_E_01.csv"
data = pd.read_csv(fichero_csv)

# Se crea un DataTable con los datos del archivo csv
tabla = dp.DataTable(data)

# Se crea una lista con los indicadores de ventas por region y año, ademas se muestra el valor negativo o positivo en
# cuanto a las ventas del 2021 con respecto del 2020

# Se un dataFrame con la suma de todas las ventas del año por region
ventas_region = data.groupby(['Región', 'Año']).sum(numeric_only=True)

regiones = ['Norte', 'Sur', 'Este', 'Oeste']
lista_indicadores = []

# Por cara region crea un BigNumber con el nombre de cada region, el valor de las ventas, el indice de cambio (resta
# de ventas de 2021 con 2020)
# y muestra el valor en verde o negro dependiendo de la condicion de que la venta del año 2021 sea mayor al 2020

for region in regiones:
    ventas_positivas = ventas_region.loc[(region, 2021), 'Ventas'] > ventas_region.loc[
        (region, 2020), 'Ventas']
    diferencia_ventas = ventas_region.loc[(region, 2021), 'Ventas'] - ventas_region.loc[
        (region, 2020), 'Ventas']
    ventas = ventas_region.loc[(region, 2021), 'Ventas']
    lista_indicadores.append(
        dp.BigNumber(heading='Región ' + region,
                     value=ventas,
                     change=diferencia_ventas,
                     is_upward_change=ventas_positivas))

titulo_pagina_2 = dp.Text('## Ventas por región del año 2021 y variación respecto a 2020')

# Agrupamos los datos de las ventas dependiento del tipo del producto y del año, calculamos la suma
ventas_ano = data.groupby(['Tipo de producto', 'Año']).sum(numeric_only=True)

graficos = []
# Por cada año de nuestro reporte crearemos un grafico con la libreria de matplotlib con las ventas de cada tipo de
# producto
for ano in range(2017, 2022):
    ventas_tipo = data[data['Año'] == ano].groupby("Tipo de producto").sum(numeric_only=True)
    grafico_matplotlib = ventas_tipo.plot.bar(y='Ventas')
    graficos.append(dp.Plot(grafico_matplotlib, responsive=False, label=str(ano)))

titulo_pagina_3 = dp.Text('## Ventas por tipo de producto para el año seleccionado')

# Creamos el reporte con una pagina dedicada a los graficos, la tabla y los valores de las ventas anuales comparada
arc = dp.Attachment(file="report_pages.html")
arc_t = dp.Text("Descargar informe")
img = dp.Media(file="DI_U05_A02_PP_E_02.png")
report = dp.App(
    dp.Page(title="Tabla",
            blocks=[tabla, arc_t,
                    arc, dp.Text("Probando poner videos"),
                    dp.Embed("https://www.youtube.com/watch?v=sBJmRD7kNTk&ab_channel=AsmrProg")]),
    dp.Page(title="Comparacion de ventas", blocks=[img, titulo_pagina_2,
                                                   dp.Group(lista_indicadores[0], lista_indicadores[1],
                                                            lista_indicadores[2],
                                                            lista_indicadores[3], arc_t,
                                                            arc, columns=1)]),
    dp.Page(title="Gráficos ventas anuales",
            blocks=[img, titulo_pagina_3, dp.Select(blocks=graficos), arc_t,
                    arc]))

report.save(path='report_pages.html', open=True)
