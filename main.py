import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Título de la aplicación
st.title('Análisis Exploratorio de Datos con Streamlit')
st.write('---')

# --- Generación de datos de ejemplo ---
@st.cache_data
def generate_data():
    """
    Genera un DataFrame de pandas con datos ficticios para el análisis.
    Los datos representan ventas mensuales de diferentes productos.
    """
    # Crear un DataFrame con datos de ventas ficticios
    data = {
        'Mes': pd.to_datetime(['2023-01', '2023-02', '2023-03', '2023-04', '2023-05',
                               '2023-06', '2023-07', '2023-08', '2023-09', '2023-10',
                               '2023-11', '2023-12', '2024-01', '2024-02', '2024-03']),
        'Producto': ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'],
        'Ventas': np.random.randint(100, 500, size=15)
    }
    df = pd.DataFrame(data)
    return df

df = generate_data()

st.header('1. Vista Previa de los Datos')
st.write('Aquí puedes ver las primeras filas de los datos que estamos analizando.')
st.dataframe(df)
st.write('---')

# --- Análisis Exploratorio de Datos (EDA) ---
st.header('2. Análisis de Datos')

# Mostrar estadísticas descriptivas
st.subheader('Estadísticas Descriptivas')
st.write(df.describe())
st.write('---')

# --- Visualizaciones ---

st.header('3. Visualizaciones')
st.write('A continuación se muestran dos gráficos para visualizar los datos.')

# Gráfico de Barras: Ventas totales por producto
st.subheader('Ventas Totales por Producto')
df_ventas_por_producto = df.groupby('Producto')['Ventas'].sum().reset_index()
fig_barras = px.bar(df_ventas_por_producto, x='Producto', y='Ventas', 
                    title='Ventas Totales por Producto')
st.plotly_chart(fig_barras)
st.write('Este gráfico de barras muestra la suma total de las ventas para cada producto.')
st.write('---')

# Gráfico de Líneas: Evolución de las ventas a lo largo del tiempo
st.subheader('Evolución de las Ventas a lo largo del tiempo')
# Asegurarse de que el eje x sea temporal para el gráfico de líneas
df_ventas_linea = df.sort_values('Mes')
fig_lineas = px.line(df_ventas_linea, x='Mes', y='Ventas', color='Producto',
                     title='Ventas Mensuales por Producto')
st.plotly_chart(fig_lineas)
st.write('Este gráfico de líneas muestra la evolución de las ventas de cada producto a lo largo del tiempo.')
st.write('---')

# --- Interacción con el usuario (ejemplo) ---
st.header('4. Interactúa con los datos')
st.write('Puedes filtrar los datos por producto para ver solo la información relevante.')

# Selector de producto en la barra lateral
producto_seleccionado = st.sidebar.selectbox(
    'Selecciona un producto:',
    df['Producto'].unique()
)

# Filtrar el DataFrame según la selección del usuario
df_filtrado = df[df['Producto'] == producto_seleccionado]

st.subheader(f'Datos para el Producto {producto_seleccionado}')
st.dataframe(df_filtrado)
