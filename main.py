import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Configuración de la página de Streamlit ---
# Se personaliza la apariencia de la página.
st.set_page_config(
    page_title="Análisis de Datos de Automóviles",
    page_icon="🚗",
    layout="wide",
)

# --- Título y descripción de la aplicación ---
st.title('Análisis Interactivo de Datos de Automóviles 🚗')
st.markdown("""
Esta aplicación permite explorar un conjunto de datos ficticio de automóviles.
Puedes filtrar los datos y visualizar diferentes métricas de forma interactiva.
""")
st.write('---')

# --- Generación de datos ficticios ---
@st.cache_data
def generate_car_data(num_rows=1000):
    """
    Genera un DataFrame de pandas con 1000 filas y 8 columnas de datos de automóviles.
    """
    marcas = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'Volkswagen', 'BMW', 'Mercedes-Benz']
    colores = ['Blanco', 'Negro', 'Gris', 'Rojo', 'Azul', 'Plata']
    combustibles = ['Gasolina', 'Diésel', 'Eléctrico']
    
    data = {
        'Marca': np.random.choice(marcas, num_rows),
        'Modelo': [f'Modelo_{i}' for i in range(num_rows)],
        'Año': np.random.randint(2015, 2024, num_rows),
        'Potencia_HP': np.random.randint(100, 500, num_rows),
        'Consumo_L_100km': np.round(np.random.uniform(5.0, 15.0, num_rows), 2),
        'Precio': np.round(np.random.uniform(20000, 150000, num_rows), 2),
        'Color': np.random.choice(colores, num_rows),
        'Tipo_Combustible': np.random.choice(combustibles, num_rows)
    }
    
    return pd.DataFrame(data)

df = generate_car_data()

# --- Barra lateral para filtros interactivos ---
st.sidebar.header('Opciones de Filtro')

# Filtro por marca
marcas_seleccionadas = st.sidebar.multiselect(
    'Selecciona una o más marcas',
    options=df['Marca'].unique(),
    default=df['Marca'].unique()
)

# Filtro por año
año_min, año_max = st.sidebar.slider(
    'Selecciona un rango de años',
    min_value=int(df['Año'].min()),
    max_value=int(df['Año'].max()),
    value=(int(df['Año'].min()), int(df['Año'].max()))
)

# Filtro por tipo de combustible
combustible_seleccionado = st.sidebar.multiselect(
    'Selecciona el tipo de combustible',
    options=df['Tipo_Combustible'].unique(),
    default=df['Tipo_Combustible'].unique()
)

# Aplicar los filtros al DataFrame
df_filtrado = df[
    (df['Marca'].isin(marcas_seleccionadas)) &
    (df['Año'] >= año_min) & (df['Año'] <= año_max) &
    (df['Tipo_Combustible'].isin(combustible_seleccionado))
]

# --- Visualización de los datos filtrados ---
st.subheader('Datos Filtrados')
st.dataframe(df_filtrado)
st.write(f"Mostrando {df_filtrado.shape[0]} de {df.shape[0]} filas.")
st.write('---')

# --- Generación de gráficos interactivos ---
st.header('Gráficos Interactivos')

# Gráfico de Barras: Precio promedio por marca
st.subheader('Precio Promedio por Marca')
df_precio_marca = df_filtrado.groupby('Marca')['Precio'].mean().reset_index()
fig_bar = px.bar(
    df_precio_marca, 
    x='Marca', 
    y='Precio',
    title='Precio Promedio de Automóviles por Marca',
    labels={'Precio': 'Precio Promedio ($)', 'Marca': 'Marca del Automóvil'},
    color='Marca'
)
st.plotly_chart(fig_bar, use_container_width=True)
st.write("Este gráfico muestra el precio promedio de los automóviles para cada marca seleccionada.")
st.write('---')

# Gráfico de Líneas: Evolución del precio promedio por año
st.subheader('Evolución del Precio Promedio por Año')
df_precio_año = df_filtrado.groupby('Año')['Precio'].mean().reset_index()
fig_line = px.line(
    df_precio_año,
    x='Año',
    y='Precio',
    title='Evolución del Precio Promedio a lo largo de los Años',
    labels={'Precio': 'Precio Promedio ($)', 'Año': 'Año del Modelo'},
)
st.plotly_chart(fig_line, use_container_width=True)
st.write("Este gráfico de líneas ilustra cómo ha cambiado el precio promedio a lo largo de los años.")
st.write('---')

# Gráfico de Dispersión: Potencia vs. Consumo
st.subheader('Potencia vs. Consumo de Combustible')
fig_scatter = px.scatter(
    df_filtrado, 
    x='Potencia_HP', 
    y='Consumo_L_100km', 
    color='Tipo_Combustible', 
    hover_data=['Marca', 'Año', 'Precio'],
    title='Relación entre Potencia y Consumo',
    labels={'Potencia_HP': 'Potencia (HP)', 'Consumo_L_100km': 'Consumo (L/100km)'}
)
st.plotly_chart(fig_scatter, use_container_width=True)
st.write("Este gráfico de dispersión muestra la relación entre la potencia y el consumo de combustible de los autos. Puedes ver los detalles al pasar el cursor sobre los puntos.")
