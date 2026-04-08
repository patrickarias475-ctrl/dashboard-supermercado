import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuración de visualización según directrices
pd.options.display.float_format = '{:,.2f}'.format

def load_data():
    # Protocolo de carga de archivos para usuario patri
    path = os.path.join(r'C:\Users\patri\Downloads', 'supermarket_sales - Sheet1.csv')
    
    # Carga con codificación específica y tipos de datos
    df = pd.read_csv(path, encoding='latin1', dtype={'ITEM_CODE': str})
    
    # Diagnóstico de verificación
    print(df.head())
    print(df.columns.tolist())
    
    # Preprocesamiento de fechas para análisis temporal
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%B')
    df['Day_Name'] = df['Date'].dt.day_name()
    df['Day_of_Week'] = df['Date'].dt.dayofweek # 0=Lunes
    return df

def main():
    st.set_page_config(page_title="Dashboard de Ventas Supermercado", layout="wide")
    st.title("📊 Análisis Avanzado de Ventas - Estándares IBCS")
    
    df = load_data()
    
    # Sidebar para filtros (Insight adicional requerido)
    st.sidebar.header("Filtros Globales")
    city_filter = st.sidebar.multiselect("Selecciona la Ciudad", options=df['City'].unique(), default=df['City'].unique())
    df_filtered = df[df['City'].isin(city_filter)]

    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Mapa de Calor Mensual", 
        "🛍️ Ventas por Ítem/Día", 
        "📈 Rendimiento Semanal",
        "💡 Insights Adicionales"
    ])

    with tab1:
        st.subheader("Mejores Meses de Ventas (Heatmap)")
        # Agrupa por mes y línea de producto
        heatmap_data = df_filtered.groupby(['Month', 'Product line'])['Total'].sum().unstack()
        fig_heat = px.imshow(heatmap_data, 
                            labels=dict(x="Línea de Producto", y="Mes", color="Ventas ($)"),
                            color_continuous_scale='Greys') # IBCS prefiere sobriedad
        st.plotly_chart(fig_heat, use_container_width=True)

    with tab2:
        st.subheader("Ventas ($) por Ítem y Día de la Semana")
        # Barras apiladas: Ítems vendidos por día
        fig_stacked = px.bar(df_filtered, 
                             x="Day_Name", 
                             y="Total", 
                             color="Product line",
                             category_orders={"Day_Name": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
                             barmode='stack',
                             template="simple_white")
        st.plotly_chart(fig_stacked, use_container_width=True)

    with tab3:
        st.subheader("Mejores Días: Ventas vs Cantidad")
        col1, col2 = st.columns(2)
        
        day_analysis = df_filtered.groupby(['Day_Name', 'Day_of_Week']).agg({
            'Total': 'sum',
            'Quantity': 'sum'
        }).reset_index().sort_values('Day_of_Week')

        with col1:
            st.write("**Total Ventas ($)**")
            st.bar_chart(data=day_analysis, x='Day_name', y='Total')
        
        with col2:
            st.write("**Total Unidades Vendidas**")
            st.bar_chart(data=day_analysis, x='Day_name', y='Quantity')

    with tab4:
        st.subheader("Insights de Rentabilidad y Género")
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Gráfico 1: Margen de beneficio por línea de producto
            fig_margin = px.box(df_filtered, x="Product line", y="gross income", 
                                title="Distribución de Ingreso Bruto por Categoría",
                                color_discrete_sequence=['#404040'])
            st.plotly_chart(fig_margin, use_container_width=True)
            
        with col_b:
            # Gráfico 2: Ventas por tipo de cliente y género
            fig_customer = px.sunburst(df_filtered, path=['Customer type', 'Gender'], values='Total',
                                       title="Segmentación de Ventas")
            st.plotly_chart(fig_customer, use_container_width=True)

    # Botón para simular la exportación (instrucción para el PDF)
    st.sidebar.markdown("---")
    if st.sidebar.button("Preparar para PDF"):
        st.sidebar.success("Usa 'Ctrl + P' y guarda como PDF para la entrega en EBAC.")

if __name__ == "__main__":
    main()
