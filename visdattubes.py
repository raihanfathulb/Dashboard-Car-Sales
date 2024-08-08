import pandas as pd
import numpy as np
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter
from bokeh.transform import cumsum, factor_cmap
from bokeh.palettes import Spectral6, Category20, Viridis256
from math import pi

car_sales_data = pd.read_csv('carsales.csv')

# Data preprocessing
car_sales_data['Latest_Launch'] = pd.to_datetime(car_sales_data['Latest_Launch'])

def car_sales_dashboard():
    st.markdown(
        """
        <div style='background-color: #bbd7dd; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <h1 style='color: white; text-align: center;'>Dashboard Penjualan Mobil</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Navigation
    page = st.sidebar.radio("Navigation", [
        "Introduction", 
        "Penjualan berdasarkan tipe mobil", 
        "Perbandingan harga dengan ukuran mesin", 
        "Merk dengan penjualan terlaris",
        "Distribusi Penjualan",
        "Distribusi Harga",
        "Perbandingan Ukuran mesin dengan Horsepower" 
    ])
    
    if page == "Introduction":
        st.markdown("""
        ## Tugas Besar Visualisasi Data
        - Muhammad Ilham Hakim S (1301210330)
        - Muhammad Darrel Prawira (1301210479)
        - Raihan Fathul Bayan (1301213272)
        - Alfiansyah Hafidz Putra Arbi (1301213240)
        """)
        st.write("Dataset ini merupakan data penjualan mobil di Amerika serikat, dengan tujuan dari project ini adalah memberikan insight bagi customer maupun brand mengenai competitive analysis, consumer preferences, market insight dan sales anaylsis. Dengan isi sebagai berikut:")
        st.write(car_sales_data.head())
        
    elif page == "Penjualan berdasarkan tipe mobil":
        st.header("Penjualan berdasarkan tipe mobil")
        st.write("Chart dibawah ini menampilkan distribusi dari tipe mobil yang laku:")

        vehicle_type_sales = car_sales_data.groupby('Vehicle_type').agg({'Sales_in_thousands': 'sum'}).reset_index()

        vehicle_type_sales['angle'] = vehicle_type_sales['Sales_in_thousands'] / vehicle_type_sales['Sales_in_thousands'].sum() * 2 * pi
        vehicle_type_sales['color'] = Spectral6[:len(vehicle_type_sales)]
        p = figure(height=350, title="Car Sales by Vehicle Type", toolbar_location=None,
                   tools="hover", tooltips="@Vehicle_type: @Sales_in_thousands", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='Vehicle_type', source=vehicle_type_sales)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None


        st.bokeh_chart(p, use_container_width=True)

    elif page == "Perbandingan harga dengan ukuran mesin":
        st.header("Perbandingan harga dengan ukuran mesin")
        st.write("Scatter plot dibawah ini menampilkan hubungan antara harga dengan ukuran mesin:")

        scatter_data = car_sales_data.dropna(subset=['Price_in_thousands', 'Engine_size'])

        source = ColumnDataSource(scatter_data)

        p = figure(title="Price vs Engine Size", height=400, width=700)
        p.scatter(x='Engine_size', y='Price_in_thousands', source=source, size=10, color='navy', alpha=0.5)

        p.xaxis.axis_label = "Engine Size"
        p.yaxis.axis_label = "Price in Thousands"

        tooltips = [("Price", "@Price_in_thousands"), ("Engine Size", "@Engine_size")]
        p.add_tools(HoverTool(tooltips=tooltips))

        st.bokeh_chart(p, use_container_width=True)

    elif page == "Merk dengan penjualan terlaris":
        st.header("Merk dengan penjualan terlaris")
        st.write("Bar chart dibawah ini menampilkan perbandingan merk mobil terlaris:")

        top_brands_sales = car_sales_data.groupby('Manufacturer').agg({'Sales_in_thousands': 'sum'}).reset_index()
        top_brands_sales = top_brands_sales.sort_values(by='Sales_in_thousands', ascending=False).head(10)

        source = ColumnDataSource(top_brands_sales)

        p = figure(x_range=top_brands_sales['Manufacturer'], height=400, title="Top 10 Car Brands by Sales",
                   toolbar_location=None, tools="")

        p.vbar(x='Manufacturer', top='Sales_in_thousands', width=0.9, source=source,
               legend_field='Manufacturer', line_color='white',
               fill_color=factor_cmap('Manufacturer', palette=Category20[len(top_brands_sales)], factors=top_brands_sales['Manufacturer']))

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.major_label_orientation = pi / 4

        st.bokeh_chart(p, use_container_width=True)

    elif page == "Distribusi Penjualan":
        st.header("Distribusi Penjualan")
        st.write("Histogram dibawah ini menampilkan distribusi penjualan mobil:")

        hist, edges = np.histogram(car_sales_data['Sales_in_thousands'], bins=20)

        p = figure(title="Distribution of Car Sales", height=400, width=700)
        p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="navy", line_color="white", alpha=0.7)

        p.xaxis.axis_label = "Sales in Thousands"
        p.yaxis.axis_label = "Count"

        st.bokeh_chart(p, use_container_width=True)

    elif page == "Distribusi Harga":
        st.header("Distribusi Harga")
        st.write("Histogram dibawah ini menampilkan distribusi harga mobil:")

        hist, edges = np.histogram(car_sales_data['Price_in_thousands'].dropna(), bins=20)

        p = figure(title="Distribution of Car Prices", height=400, width=700)
        p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="green", line_color="white", alpha=0.7)

        p.xaxis.axis_label = "Price in Thousands"
        p.yaxis.axis_label = "Count"

        st.bokeh_chart(p, use_container_width=True)

    elif page == "Perbandingan Ukuran mesin dengan Horsepower":
        st.header("Perbandingan Ukuran mesin dengan Horsepower")
        st.write("Scatter plot dibawah ini menampilkan hubungan antara ukuran mesin dengan horsepower: ")

        scatter_data = car_sales_data.dropna(subset=['Engine_size', 'Horsepower'])

        source = ColumnDataSource(scatter_data)

        p = figure(title="Engine Size vs Horsepower", height=400, width=700)
        p.scatter(x='Engine_size', y='Horsepower', source=source, size=10, color='purple', alpha=0.6)

        p.xaxis.axis_label = "Engine Size"
        p.yaxis.axis_label = "Horsepower"

        tooltips = [("Engine Size", "@Engine_size"), ("Horsepower", "@Horsepower")]
        p.add_tools(HoverTool(tooltips=tooltips))

        st.bokeh_chart(p, use_container_width=True)

if __name__ == "__main__":
    car_sales_dashboard()