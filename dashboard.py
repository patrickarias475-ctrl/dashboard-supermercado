import streamlit as st
import pandas as pd
import os

# El script configura el formato general para los números flotantes.
pd.options.display.float_format = '{:,.2f}'.format

# El sistema define la ruta del archivo apuntando a la carpeta de descargas.
ruta_archivo = os.path.join(r"C:\Users\patri\Downloads", "supermarket_sales.csv")

# El código realiza la carga del archivo.
df = pd.read_csv(ruta_archivo, encoding='latin1', dtype={'ITEM_CODE': str})

# 1. Para ver los datos
print(df.head())

# 2. Para ver los nombres EXACTOS de las columnas (sin recortes)
print(df.columns.tolist())

# El programa configura la página web principal.
st.set_page_config(page_title="Wireframes EBAC", layout="wide")
st.title("Wireframes de Dashboards - Análisis de Supermercado")

# La interfaz crea las cuatro pestañas solicitadas.
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Ventas y Factura", 
    "2. Volumen y Clientes", 
    "3. Ranking Top 10", 
    "4. KPIs Generales"
])

with tab1:
    st.header("Reporte de Ventas y Factura Promedio")
    col1, col2, col3 = st.columns(3)
    col1.selectbox("Filtro: Fecha", ["Todas", "1/5/2019", "2/8/2019"])
    col2.selectbox("Filtro: Mes", ["Enero", "Febrero", "Marzo"])
    col3.selectbox("Filtro: Product line", df['Product line'].unique())
    
    st.markdown("---")
    col_graf, col_kpi = st.columns([3, 1])
    with col_graf:
        st.subheader("Evolución de las ventas (Total)")
        st.line_chart(df['Total'][:20]) 
    with col_kpi:
        st.metric(label="Factura Promedio", value="$322.97")

with tab2:
    st.header("Total Número de Ventas y Clientes Mensuales")
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(label="Total de Facturas", value="1,000")
    kpi2.metric(label="Clientes Únicos", value="450")
    st.bar_chart(df['Total'][:15])

with tab3:
    st.header("Ranking: Top 10 Ítems Más Vendidos")
    st.bar_chart(df['Quantity'].value_counts()[:10])

with tab4:
    st.header("Dashboard de KPIs Generales")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric(label="Venta Total", value="$322,966.75")
    k2.metric(label="Ticket Promedio", value="$322.97")
    k3.metric(label="Total Unidades", value="5,510")
    k4.metric(label="Margen Bruto", value="4.76%")
    st.dataframe(df[['Product line', 'Total']].head(5))