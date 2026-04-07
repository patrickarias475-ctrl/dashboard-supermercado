import streamlit as st
import pandas as pd
import os

# El script configura el formato general para los números flotantes.
pd.options.display.float_format = '{:,.2f}'.format

# El sistema define la ruta del archivo apuntando a la carpeta de descargas.
ruta_archivo = "supermarket_sales.csv"

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

import streamlit as st
import pandas as pd
import os

# El intérprete configura siempre el formato general.
pd.options.display.float_format = '{:,.2f}'.format

# La aplicación establece la configuración de la página para aprovechar el ancho del monitor.
st.set_page_config(page_title="Panel de Ventas EBAC", layout="wide")

# El sistema define la ruta apuntando estrictamente al directorio de descargas local.
ruta_archivo = os.path.join(r"C:\Users\patri\Downloads", "supermarket_sales_M23 y M40 (1).csv")

# El script ejecuta el protocolo de carga con la codificación y tipo de dato requeridos.
df = pd.read_csv(ruta_archivo, encoding='latin1', dtype={'ITEM_CODE': str})

# Python # 1. Para ver los datos
print(df.head())

# Python # 2. Para ver los nombres EXACTOS de las columnas (sin recortes)
print(df.columns.tolist())

# El programa transforma la columna de fechas para habilitar los análisis temporales.
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
    
    # El script procesa el filtro de fechas evitando errores de selección vacía.
    min_date, max_date = df['Date'].min(), df['Date'].max()
    filtro_fecha_t1 = col_f3.date_input("Filtrar Rango de Fechas", value=(min_date, max_date), key='f1')
    
    # El sistema aplica los filtros al dataframe.
    df_t1 = df[
        (df['Month'].isin(filtro_mes_t1)) & 
        (df['Product line'].isin(filtro_item_t1))
    ]
    
    # La herramienta proyecta las métricas principales de la pestaña.
    m1, m2 = st.columns(2)
    m1.metric("Ventas Totales", f"${df_t1['Total'].sum():,.2f}")
    m2.metric("Factura Promedio", f"${df_t1['Total'].mean():,.2f}")
    
    # El programa renderiza la tabla de detalles financieros.
    st.dataframe(df_t1[['Date', 'Invoice ID', 'Product line', 'Total']], use_container_width=True)

# ==========================================
# PESTAÑA 2: Volumetría y clientes
# ==========================================
with tab2:
    st.subheader("Total Número de Ventas y Clientes Mensuales")
    
    # El filtro local controla la visualización del mes.
    filtro_mes_t2 = st.multiselect("Filtrar Meses", options=df['Month'].unique(), default=df['Month'].unique(), key='m2')
    df_t2 = df[df['Month'].isin(filtro_mes_t2)]
    
    # El algoritmo calcula las volumetrías operativas agrupadas por mes.
    volumetria = df_t2.groupby('Month').agg(
        Total_Ventas=('Invoice ID', 'count'),
        Clientes_Unicos=('Invoice ID', 'nunique')
    ).reset_index()
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.dataframe(volumetria, use_container_width=True)
    with col_v2:
        # El sistema grafica el volumen de ventas respetando el formato IBCS (barras simples).
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
    
    # El código agrupa y extrae estrictamente los 10 registros superiores según el criterio.
    top_10 = df_t3.groupby('Product line')[criterio_t3].sum().nlargest(10).reset_index()
    
    # La aplicación presenta los datos de forma analítica y visual.
    st.dataframe(top_10, use_container_width=True)
    st.bar_chart(data=top_10.set_index('Product line'), horizontal=True)

# ==========================================
# PESTAÑA 4: Reporte de KPIs Generales
# ==========================================
with tab4:
    st.subheader("Indicadores Clave de Rendimiento (KPIs)")
    
    # El usuario controla el alcance general mediante este filtro.
    filtro_mes_t4 = st.multiselect("Filtro Global (Mes)", options=df['Month'].unique(), default=df['Month'].unique(), key='m4')
    df_t4 = df[df['Month'].isin(filtro_mes_t4)]
    
    k1, k2 = st.columns(2)
    # 1) Venta total
    k1.metric("1) Venta Total Global", f"${df_t4['Total'].sum():,.2f}")
    # 2) Ticket promedio total
    k2.metric("2) Ticket Promedio Global", f"${df_t4['Total'].mean():,.2f}")
    
    st.markdown("---")
    col_k3, col_k4 = st.columns(2)
    
    with col_k3:
        st.write("**3) Ranking TOP 20 - Ventas Totales**")
        # El programa aísla los 20 elementos de mayor impacto en ingresos.
        top_20_ventas = df_t4.groupby('Product line')['Total'].sum().nlargest(20).reset_index()
        st.dataframe(top_20_ventas, use_container_width=True)
        
    with col_k4:
        st.write("**4) Ranking Total - Unidades Vendidas**")
        # El script ordena el catálogo completo por desplazamiento de inventario.
        top_unidades = df_t4.groupby('Product line')['Quantity'].sum().sort_values(ascending=False).reset_index()
        st.dataframe(top_unidades, use_container_width=True)
