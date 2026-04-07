import streamlit as st
import pandas as pd
import altair as alt

# El intérprete configura el formato general para los números flotantes.
pd.options.display.float_format = '{:,.2f}'.format

# El sistema establece la configuración de la página y oculta el menú predeterminado para mayor limpieza.
st.set_page_config(page_title="Panel de Ventas Institucional", layout="wide")

# El script define la ruta relativa para el entorno en la nube.
ruta_archivo = "supermarket_sales_M23 y M40 (1).csv"

# La aplicación ejecuta la carga del archivo en formato estándar.
df = pd.read_csv(ruta_archivo, encoding='utf-8', dtype={'ITEM_CODE': str})

# 1. Para ver los datos
print(df.head())

# 2. Para ver los nombres EXACTOS de las columnas
print(df.columns.tolist())

# El programa transforma la columna de fechas para habilitar análisis temporales.
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month

# La interfaz dibuja el título general con una estructura jerárquica clara.
st.title("Reporte Operativo y Financiero de Ventas")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Análisis de Facturación", 
    "2. Volumetría Temporal", 
    "3. Ranking Categórico", 
    "4. KPIs Estratégicos"
])

# ==========================================
# PESTAÑA 1: Reporte de ventas y factura
# ==========================================
with tab1:
    st.subheader("Ingresos y Facturación Promedio")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    filtro_mes_t1 = col_f1.multiselect("Filtro: Mes", options=df['Month'].unique(), default=df['Month'].unique(), key='m1')
    filtro_item_t1 = col_f2.multiselect("Filtro: Línea de Producto", options=df['Product line'].unique(), default=df['Product line'].unique(), key='i1')
    
    min_date, max_date = df['Date'].min(), df['Date'].max()
    filtro_fecha_t1 = col_f3.date_input("Filtro: Rango de Fechas", value=(min_date, max_date), key='f1')
    
    # El algoritmo aplica los parámetros de reducción al dataframe.
    df_t1 = df[
        (df['Month'].isin(filtro_mes_t1)) & 
        (df['Product line'].isin(filtro_item_t1))
    ]
    
    m1, m2 = st.columns(2)
    m1.metric("Ventas Totales Netas", f"${df_t1['Total'].sum():,.2f}")
    m2.metric("Valor del Ticket Promedio", f"${df_t1['Total'].mean():,.2f}")
    
    st.dataframe(df_t1[['Date', 'Invoice ID', 'Product line', 'Total']], use_container_width=True)

# ==========================================
# PESTAÑA 2: Volumetría y clientes
# ==========================================
with tab2:
    st.subheader("Volumen Operativo por Periodo")
    
    filtro_mes_t2 = st.multiselect("Selección de Periodo", options=df['Month'].unique(), default=df['Month'].unique(), key='m2')
    df_t2 = df[df['Month'].isin(filtro_mes_t2)]
    
    # El código consolida las métricas de tráfico.
    volumetria = df_t2.groupby('Month').agg(
        Total_Ventas=('Invoice ID', 'count'),
        Clientes_Unicos=('Invoice ID', 'nunique')
    ).reset_index()
    
    col_v1, col_v2 = st.columns([1, 2])
    with col_v1:
        st.dataframe(volumetria, use_container_width=True)
    with col_v2:
        # El sistema grafica series de tiempo mediante columnas verticales sobrias, eliminando cuadrículas.
        grafico_volumen = alt.Chart(volumetria).mark_bar(color='#595959', size=40).encode(
            x=alt.X('Month:O', title='', axis=alt.Axis(labelAngle=0, grid=False)),
            y=alt.Y('Total_Ventas:Q', title='', axis=alt.Axis(grid=False)),
            tooltip=['Month', 'Total_Ventas']
        ).configure_view(strokeWidth=0).properties(height=350)
        
        st.altair_chart(grafico_volumen, use_container_width=True)

# ==========================================
# PESTAÑA 3: Ranking TOP 10 mensual
# ==========================================
with tab3:
    st.subheader("Ranking de Desplazamiento por Línea de Producto")
    
    col_r1, col_r2 = st.columns(2)
    filtro_mes_t3 = col_r1.selectbox("Mes de Evaluación", options=df['Month'].unique(), key='m3')
    criterio_t3 = col_r2.selectbox("Métrica Base", options=['Total', 'Quantity'], key='c3')
    
    df_t3 = df[df['Month'] == filtro_mes_t3]
    
    # El script aísla la muestra superior para el análisis categórico.
    top_10 = df_t3.groupby('Product line')[criterio_t3].sum().nlargest(10).reset_index()
    
    col_r3, col_r4 = st.columns([1, 2])
    with col_r3:
        st.dataframe(top_10, use_container_width=True)
    with col_r4:
        # El programa genera barras horizontales estructuradas en orden descendente, estándar para categorías.
        grafico_ranking = alt.Chart(top_10).mark_bar(color='#404040').encode(
            x=alt.X(f'{criterio_t3}:Q', title='', axis=alt.Axis(grid=False)),
            y=alt.Y('Product line:N', title='', sort='-x', axis=alt.Axis(labelLimit=200, grid=False)),
            tooltip=['Product line', criterio_t3]
        ).configure_view(strokeWidth=0).properties(height=350)
        
        st.altair_chart(grafico_ranking, use_container_width=True)

# ==========================================
# PESTAÑA 4: Reporte de KPIs Generales
# ==========================================
with tab4:
    st.subheader("Tablero de Indicadores de Rendimiento")
    
    filtro_mes_t4 = st.multiselect("Cobertura Temporal", options=df['Month'].unique(), default=df['Month'].unique(), key='m4')
    df_t4 = df[df['Month'].isin(filtro_mes_t4)]
    
    k1, k2 = st.columns(2)
    k1.metric("1) Ingreso Operativo Total", f"${df_t4['Total'].sum():,.2f}")
    k2.metric("2) Ticket Promedio Consolidado", f"${df_t4['Total'].mean():,.2f}")
    
    st.markdown("---")
    col_k3, col_k4 = st.columns(2)
    
    with col_k3:
        st.markdown("##### 3) Impacto de Ingresos (TOP 20)")
        top_20_ventas = df_t4.groupby('Product line')['Total'].sum().nlargest(20).reset_index()
        st.dataframe(top_20_ventas, use_container_width=True)
        
    with col_k4:
        st.markdown("##### 4) Rotación de Inventario (Total)")
        top_unidades = df_t4.groupby('Product line')['Quantity'].sum().sort_values(ascending=False).reset_index()
        st.dataframe(top_unidades, use_container_width=True)
