import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Establece el formato general de visualización.
pd.options.display.float_format = '{:,.2f}'.format

@st.cache_data
def load_data():
    # Define las rutas para entorno local y nube.
    local_path = os.path.join(r'C:\Users\patri\Downloads', 'supermarket_sales - Sheet1.csv')
    cloud_path = 'supermarket_sales - Sheet1.csv' 
    
    # Evalúa el entorno para asignar la ruta.
    if os.path.exists(local_path):
        path = local_path
    else:
        path = cloud_path
        
    # Ejecuta el protocolo de carga de archivos.
    df = pd.read_csv(path, encoding='UTF-8', dtype={'ITEM_CODE': str})
    
    # Ejecuta el diagnóstico de verificación.
    print(df.head())
    print(df.columns.tolist())
    
    # Procesa las fechas para el análisis temporal.
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%B')
    df['Day_Name'] = df['Date'].dt.day_name()
    df['Day_of_Week'] = df['Date'].dt.dayofweek 
    return df

def main():
    # Configura la página principal.
    st.set_page_config(page_title="Dashboard de Ventas", layout="wide")
    st.title("Análisis Avanzado de Ventas (Estándares IBCS)")
    
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Error: El archivo CSV no se encuentra. Asegúrate de que 'supermarket_sales - Sheet1.csv' esté en el repositorio.")
        st.stop()
    
    # Genera los filtros globales en la barra lateral.
    st.sidebar.header("Filtros Globales")
    city_filter = st.sidebar.multiselect("Ciudad", options=df['City'].unique(), default=df['City'].unique())
    df_filtered = df[df['City'].isin(city_filter)]

    # Crea las pestañas de navegación.
    tab1, tab2, tab3, tab4 = st.tabs([
        "Mapa de Calor Mensual", 
        "Ventas por Ítem/Día", 
        "Rendimiento Semanal",
        "Insights Adicionales"
    ])

    with tab1:
        st.subheader("Mejores Meses de Ventas por Línea de Producto")
        # Genera la matriz de datos para el mapa de calor.
        heatmap_data = df_filtered.groupby(['Month', 'Product line'])['Total'].sum().unstack()
        fig_heat = px.imshow(heatmap_data, 
                            labels=dict(x="Línea de Producto", y="Mes", color="Ventas Totales ($)"),
                            color_continuous_scale='Greys') 
        st.plotly_chart(fig_heat, use_container_width=True)

    with tab2:
        st.subheader("Ventas en ($) por Día de la Semana y Línea de Producto")
        # Genera el gráfico de barras apiladas.
        fig_stacked = px.bar(df_filtered, 
                             x="Day_Name", 
                             y="Total", 
                             color="Product line",
                             category_orders={"Day_Name": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
                             barmode='stack',
                             color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_stacked, use_container_width=True)

    with tab3:
        st.subheader("Mejores Días: Ventas Totales vs Cantidad de Ítems")
        col1, col2 = st.columns(2)
        
        # Agrupa los datos por día de la semana.
        day_analysis = df_filtered.groupby(['Day_Name', 'Day_of_Week']).agg({
            'Total': 'sum',
            'Quantity': 'sum'
        }).reset_index().sort_values('Day_of_Week')

        with col1:
            st.write("**Total Ventas ($)**")
            st.bar_chart(data=day_analysis, x='Day_Name', y='Total', color="#404040")
        
        with col2:
            st.write("**Total Unidades Vendidas**")
            st.bar_chart(data=day_analysis, x='Day_Name', y='Quantity', color="#808080")

    with tab4:
        st.subheader("Análisis de Demografía y Pagos")
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Construye el gráfico de distribución por género.
            fig_gender = px.pie(df_filtered, values='Total', names='Gender', 
                                title="Distribución de Ventas por Género",
                                color_discrete_sequence=['#404040', '#A0A0A0'])
            st.plotly_chart(fig_gender, use_container_width=True)
            
        with col_b:
            # Construye el gráfico de métodos de pago.
            fig_payment = px.histogram(df_filtered, x="Payment", y="Total",
                                       title="Ventas por Método de Pago",
                                       color_discrete_sequence=['#606060'])
            st.plotly_chart(fig_payment, use_container_width=True)

if __name__ == "__main__":
    main()
