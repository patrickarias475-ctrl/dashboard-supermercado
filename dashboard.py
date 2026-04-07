import streamlit as st
import pandas as pd
import altair as alt
from datetime import date

# El intérprete configura el formato general para los números flotantes.
pd.options.display.float_format = '{:,.2f}'.format

# El sistema establece la configuración de la página y oculta elementos innecesarios.
st.set_page_config(page_title="Reporte de Ventas", layout="wide")

# El script define la ruta relativa para el entorno en la nube.
ruta_archivo = "supermarket_sales_M23 y M40 (1).csv"

# La aplicación ejecuta la carga del archivo asegurando la lectura correcta.
df = pd.read_csv(ruta_archivo, encoding='utf-8', dtype={'ITEM_CODE': str})

# 1. Para ver los datos
print(df.head())

# 2. Para ver los nombres EXACTOS de las columnas
print(df.columns.tolist())

# El programa procesa la columna temporal para habilitar las comparaciones.
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month

# ==========================================
# ENCABEZADO INSTITUCIONAL (Norma IBCS)
# ==========================================
st.title("Reporte Operativo y Financiero de Ventas")
st.markdown("**Entidad:** Cadena de Supermercados | **Unidad:** Consolidado Nacional | **Moneda:** USD")
st.caption(f"📅 Fecha de emisión: {date.today().strftime('%d/%m/%Y')} | 👤 Analista: Patrick Salvador Hernández Arias | 📚 Fuente: Kaggle")
st.markdown("---")

# ==========================================
# ZONA DE FILTROS GLOBALES (Clásicos)
# ==========================================
# ==========================================
# ZONA DE FILTROS GLOBALES (Clásicos)
# ==========================================
col_f1, col_f2, col_f3 = st.columns(3)

# El sistema crea listas de opciones incluyendo el valor 'Todos' por defecto.
opciones_mes = ["Todos"] + sorted(df['Month'].unique().tolist())
opciones_item = ["Todas"] + sorted(df['Product line'].unique().tolist())

filtro_mes = col_f1.selectbox("Filtro: Mes", options=opciones_mes)
filtro_item = col_f2.selectbox("Filtro: Línea de Producto", options=opciones_item)

min_date, max_date = df['Date'].min().date(), df['Date'].max().date()
filtro_fecha = col_f3.date_input("Filtro: Rango de Fechas", value=(min_date, max_date))

# El algoritmo evalúa y aplica los filtros seleccionados de forma dinámica.
df_filtrado = df.copy()

if filtro_mes != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Month'] == filtro_mes]

if filtro_item != "Todas":
    df_filtrado = df_filtrado[df_filtrado['Product line'] == filtro_item]

# El script corrige el comportamiento de lectura de la tupla de fechas.
if isinstance(filtro_fecha, (tuple, list)):
    if len(filtro_fecha) == 2:
        # El usuario seleccionó correctamente inicio y fin.
        start_date, end_date = filtro_fecha
        df_filtrado = df_filtrado[(df_filtrado['Date'].dt.date >= start_date) & (df_filtrado['Date'].dt.date <= end_date)]
    elif len(filtro_fecha) == 1:
        # El usuario hizo el primer clic; el sistema filtra solo por ese día exacto.
        start_date = filtro_fecha[0]
        df_filtrado = df_filtrado[df_filtrado['Date'].dt.date == start_date]

# ==========================================
# ESTRUCTURA DE PESTAÑAS
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "1. Resumen Ejecutivo (KPIs y Facturación)", 
    "2. Volumetría Operativa", 
    "3. Ranking de Categorías"
])

# ==========================================
# PESTAÑA 1: KPIs y Facturación
# ==========================================
with tab1:
    st.subheader("Indicadores Clave de Rendimiento")
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Ingreso Operativo Total", f"${df_filtrado['Total'].sum():,.2f}")
    k2.metric("Ticket Promedio Consolidado", f"${df_filtrado['Total'].mean():,.2f}")
    k3.metric("Total de Operaciones", f"{len(df_filtrado):,}")
    
    st.markdown("---")
    st.subheader("Desglose de Facturación")
    st.dataframe(df_filtrado[['Date', 'Invoice ID', 'Product line', 'Total']], use_container_width=True)

# ==========================================
# PESTAÑA 2: Volumetría y clientes
# ==========================================
with tab2:
    st.subheader("Volumen Operativo Temporal")
    
    # El código consolida las métricas de tráfico.
    volumetria = df_filtrado.groupby('Month').agg(
        Total_Ventas=('Invoice ID', 'count'),
        Clientes_Unicos=('Invoice ID', 'nunique')
    ).reset_index()
    
    col_v1, col_v2 = st.columns([1, 2])
    with col_v1:
        st.dataframe(volumetria, use_container_width=True)
    with col_v2:
        # El sistema grafica usando columnas verticales en escala de grises.
        grafico_volumen = alt.Chart(volumetria).mark_bar(color='#595959', size=40).encode(
            x=alt.X('Month:O', title='Mes del Año', axis=alt.Axis(labelAngle=0, grid=False)),
            y=alt.Y('Total_Ventas:Q', title='Número de Ventas', axis=alt.Axis(grid=False)),
            tooltip=['Month', 'Total_Ventas']
        ).configure_view(strokeWidth=0).properties(height=350)
        
        st.altair_chart(grafico_volumen, use_container_width=True)

# ==========================================
# PESTAÑA 3: Ranking Categórico
# ==========================================
with tab3:
    st.subheader("Desplazamiento por Línea de Producto (TOP 10)")
    
    criterio_t3 = st.selectbox("Métrica Base para el Ranking", options=['Total', 'Quantity'])
    
    # El script aísla la muestra superior respetando los filtros globales.
    top_10 = df_filtrado.groupby('Product line')[criterio_t3].sum().nlargest(10).reset_index()
    
    col_r1, col_r2 = st.columns([1, 2])
    with col_r1:
        st.dataframe(top_10, use_container_width=True)
    with col_r2:
        # El programa renderiza barras horizontales para datos categóricos (Norma IBCS).
        grafico_ranking = alt.Chart(top_10).mark_bar(color='#404040').encode(
            x=alt.X(f'{criterio_t3}:Q', title='Valor', axis=alt.Axis(grid=False)),
            y=alt.Y('Product line:N', title='', sort='-x', axis=alt.Axis(labelLimit=200, grid=False)),
            tooltip=['Product line', criterio_t3]
        ).configure_view(strokeWidth=0).properties(height=350)
        
        st.altair_chart(grafico_ranking, use_container_width=True)
