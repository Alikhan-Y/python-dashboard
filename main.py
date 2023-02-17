#  To run the web app type: streamlit run main.py
# Importing librarires python 
import pandas as pd # python -m pip install pandas openpyxl
import plotly.express as px # python -m pip install plotly.express
import streamlit as st # python -m pip install streamlit

#  Configuring the web app 
st.set_page_config(page_title='Sales Dashboard', 
                   page_icon=':bar_chart:', 
                   layout="wide")

# Converting Excel file to pandas format
# To not rerun the dataset each time we change filters, we can cache the dataframe 
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(io='supermarket_sales.xlsx',
                    engine='openpyxl',
                    sheet_name='Sales',
                    skiprows=3,
                    usecols='B:R',
                    nrows=1000)

    # Adding 'Hour' column to the dataframe
    df['hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    return df
df = get_data_from_excel()


#  ---- Sidebar ---- 
st.sidebar.header('Filters')
city = st.sidebar.multiselect('Select the City:',
                              options=df['City'].unique(),
                              default=df['City'].unique())

customer_type = st.sidebar.multiselect('Select Customer Type:',
                              options=df['Customer_type'].unique(),
                              default=df['Customer_type'].unique())

gender = st.sidebar.multiselect('Select Gender:',
                              options=df['Gender'].unique(),
                              default=df['Gender'].unique())

#  Query method to filter data
df_selection = df.query("City == @city & Customer_type == @customer_type & Gender == @gender")

#  To display filtered dataframe onto the page 
# st.dataframe(df_selection)


#  ---- Main Page ---- to replace dataset 
st.title(':bar_chart: Sales Dashboard')
st.markdown('##')

# Top KPI`s
total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection['Rating'].mean(), 1)
star_rating = ':star:' * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection['Total'].mean(), 2)

# Creating oclumns
left_column, middle_column, right_column = st.columns(3)

# Inserting values into oclumns
with left_column:
    st.subheader("Total Sales")
    st.subheader(f'US $ {total_sales:,}')

with middle_column:
    st.subheader("Average Rating")
    st.subheader(f'{average_rating} {star_rating}')

with right_column:
    st.subheader("Average Sales per Transation")
    st.subheader(f'US $ {average_sale_by_transaction:,}')
    
# To separate from the next section
st.markdown('---')

# ---- Barcharts ----
# Sales by Product Line (Bar Chart)
# Using pandas group by method 
sales_by_product_line = (
    df_selection.groupby(by=['Product line']).sum()[['Total']].sort_values(by='Total')
)
# Creating the chart
fig_product_sales = px.bar(
    sales_by_product_line,
    x='Total',
    y=sales_by_product_line.index,
    orientation='h',
    title='<b>Sales by Product Line</b>',
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template='plotly_white'
)
# tweaking the chart so the bg colour is transparent and no grid on the x axis
fig_product_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
)

# to diplay the chart
# st.plotly_chart(fig_product_sales)

# Sales by Hour (Bar Chart)
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[['Total']]

# Creating the chart
fig_sales_by_hour = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y='Total',
    title='<b>Sales by Hour</b>',
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template='plotly_white'
)
# tweaking the chart so the bg colour is transparent and no grid on the x axis
fig_sales_by_hour.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=(dict(showgrid=False))
)

# to display the chart
# st.plotly_chart(fig_sales_by_hour)

# Displaying 2 charts besides each otehr
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_sales_by_hour, use_container_width=True)


# ---- Hide Streamlit Style ---- USING CSS
hide_st_style = """
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility:hidden;}
            header {visibility:hidden;}
            </style>   
            """
st.markdown(hide_st_style, unsafe_allow_html=True)