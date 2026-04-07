import streamlit as st
import pandas as pd
import os

# El intérprete configura el formato general para los números flotantes.
pd.options.display.float_format = '{:,.2f}'.format

# El sistema establece la configuración de la página.
st.set_page_config(page_title="Panel de Ventas EBAC", layout="wide")

# El script define la ruta relativa para compatibilidad con el servidor de la nube.
ruta_archivo = "supermarket_sales_M23 y M40 (1).csv"

# La aplicación ejecuta la carga del archivo usando la codificación correcta.
df = pd.read_csv(ruta_archivo, encoding='utf-8', dtype={'ITEM_CODE': str})

# 1. Para ver los datos (Este diagnóstico se imprimirá en los logs de la nube)
print(df.head())

# 2. Para ver los nombres EXACTOS de las columnas
print(df.columns.tolist())

# El programa transforma la columna de fechas para habilitar análisis temporales.
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month

# La interfaz dibuja el título general del tablero.
st.title("Panel de Control Operativo y Financiero")

# El sistema construye las cuatro pestañas exigidas por la rúbrica.
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Ventas y Factura", 
    "2. Volumetría de Clientes", 
    "3. Ranking TOP 10", 
    "4. KPIs Generales"
])

# ==========================================
# PESTAÑA 1: Reporte de ventas y factura
# ==========================================
with tab1:
    st.subheader("Reporte de Ventas y Factura Promedio")
    
    # El algoritmo despliega los filtros de esta vista.
    col_f1, col_f2, col_f3 = st.columns(3)
    filtro_mes_t1 = col_f1.multiselect("Filtrar Mes", options=df['Month'].unique(), default=df['Month'].unique(), key='m1')
    filtro_item_t1 = col_f2.multiselect("Filtrar Ítem", options=df['Product line'].unique(), default=df['Product line'].unique(), key='i1')
    
    min_date, max_date = df['Date'].min(), df['Date'].max()
    filtro_fecha_t1 = col_f3.date_input("Filtrar Rango de Fechas", value=(min_date, max_date), key='f1')
    
    # El script aplica los filtros.
    df_t1 = df[
        (df['Month'].isin(filtro_mes_t1)) & 
        (df['Product line'].isin(filtro_item_t1))
    ]
    
    m1, m2 = st.columns(2)
    m1.metric("Ventas Totales", f"${df_t1['Total'].sum():,.2f}")
    m2.metric("Factura Promedio", f"${df_t1['Total'].mean():,.2f}")
    
    st.dataframe(df_t1[['Date', 'Invoice ID', 'Product line', 'Total']], use_container_width=True)

# ==========================================
# PESTAÑA 2: Volumetría y clientes
# ==========================================
with tab2:
    st.subheader("Total Número de Ventas y Clientes Mensuales")
    
    filtro_mes_t2 = st.multiselect("Filtrar Meses", options=df['Month'].unique(), default=df['Month'].unique(), key='m2')
    df_t2 = df[df['Month'].isin(filtro_mes_t2)]
    
    # El programa calcula las volumetrías operativas.
    volumetria = df_t2.groupby('Month').agg(
        Total_Ventas=('Invoice ID', 'count'),
        Clientes_Unicos=('Invoice ID', 'nunique')
    ).reset_index()
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.dataframe(volumetria, use_container_width=True)
    with col_v2:
        st.bar_chart(data=volumetria, x='Month', y='Total_Ventas')

# ==========================================
# PESTAÑA 3: Ranking TOP 10 mensual
# ==========================================
with tab3:
    st.subheader("Ranking TOP 10 Mensual de Ítems")
    
    col_r1, col_r2 = st.columns(2)
    filtro_mes_t3 = col_r1.selectbox("Seleccionar Mes a Evaluar", options=df['Month'].unique(), key='m3')
    criterio_t3 = col_r2.selectbox("Criterio de Evaluación", options=['Total', 'Quantity'], key='c3')
    
    df_t3 = df[df['Month'] == filtro_mes_t3]
    
    # El código aísla los 10 registros superiores.
    top_10 = df_t3.groupby('Product line')[criterio_t3].sum().nlargest(10).reset_index()
    
    st.dataframe(top_10, use_container_width=True)
    st.bar_chart(data=top_10.set_index('Product line'), horizontal=True)

# ==========================================
# PESTAÑA 4: Reporte de KPIs Generales
# ==========================================
with tab4:
    st.subheader("Indicadores Clave de Rendimiento (KPIs)")
    
    filtro_mes_t4 = st.multiselect("Filtro Global (Mes)", options=df['Month'].unique(), default=df['Month'].unique(), key='m4')
    df_t4 = df[df['Month'].isin(filtro_mes_t4)]
    
    k1, k2 = st.columns(2)
    k1.metric("1) Venta Total Global", f"${df_t4['Total'].sum():,.2f}")
    k2.metric("2) Ticket Promedio Global", f"${df_t4['Total'].mean():,.2f}")
    
    st.markdown("---")
    col_k3, col_k4 = st.columns(2)
    
    with col_k3:
        st.write("**3) Ranking TOP 20 - Ventas Totales**")
        top_20_ventas = df_t4.groupby('Product line')['Total'].sum().nlargest(20).reset_index()
        st.dataframe(top_20_ventas, use_container_width=True)
        
    with col_k4:
        st.write("**4) Ranking Total - Unidades Vendidas**")
        top_unidades = df_t4.groupby('Product line')['Quantity'].sum().sort_values(ascending=False).reset_index()
        st.dataframe(top_unidades, use_container_width=True)
