import pandas as pd
import datapane as dp

# Cargar los datos del informe en un dataframe de pandas
data = pd.read_csv('DI_U05_A02_PP_E_01.csv')

# Calcular el importe total de ventas del año 2021 y del año anterior
ventas_2021 = data[data['Año'] == 2021]['Ventas'].sum()
ventas_anterior = data[data['Año'] == 2020]['Ventas'].sum()
variacion_ventas = (ventas_2021 - ventas_anterior) / ventas_anterior

# Crear una tabla con los datos del informe
tabla = dp.Table(data)

# Crear un informe con los elementos requeridos
report = dp.App(
    dp.Group(
        dp.Select(
            dp.Text(f'Importe total de ventas en 2021: {ventas_2021:,.2f} €'),
            dp.Text(f'Variación respecto al año anterior: {variacion_ventas:.2%}'),
            tabla, name="Reporte_Ventas", label="label_reporte"
        )
    )
)
report.save(path="my_report.html")

# Publicar el informe en la plataforma de Datapane

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
