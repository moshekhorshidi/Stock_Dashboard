import pandas as pd
import streamlit as st 
import plotly.express as px
import plotly.graph_objects as go


# -- set my web page -- 
st.set_page_config(page_title='Moshe Khorshidi home test app dashboard',
                   page_icon=':star:',
                   layout='wide') # wide window for my app 

# -- data load and manage
# after download a csv from snowflake, insert into a data frame 
# for better usage i'll cash the data

@st.cache_data
def dataframe_cashed_read(file):
    data = pd.read_csv(file)
    return data

# one time read to cash

user_input_file = st.sidebar.file_uploader("Upload Result_Data.csv Data file")
if user_input_file is None:
    st.info("Please Upload result_data.csv file provided")
    st.stop()

df = dataframe_cashed_read(user_input_file)

# -- data type convert 
df['RANKING'] = df['RANKING'].astype(int)
df['SEASONAL_DATE_TO_ANALYZE'] = pd.to_datetime(df['SEASONAL_DATE_TO_ANALYZE']).dt.date
df['ON_YEAR'] = df['ON_YEAR'].astype(str)
df['ON_MONTH'] = df['ON_MONTH'].astype(str)
df['ON_DAY'] = df['ON_DAY'].astype(str)
df['THE_QUARTER_TO_MATCH_AND_ANALYZE'] = df['THE_QUARTER_TO_MATCH_AND_ANALYZE'].astype(str)
df['STORE_TO_ANALYZE_AND_REPLICATE_MARKTING'] = df['STORE_TO_ANALYZE_AND_REPLICATE_MARKTING'].astype(str)
df['NEW_TARGET_RANGE_TOP_BOUNDARY'] = df['NEW_TARGET_RANGE_TOP_BOUNDARY'].astype(float)

# -- sidebar for filtering df -- 

st.sidebar.header("Filter data and visual:")
st.sidebar.subheader("The filters are a and (&) relationship")

year = st.sidebar.multiselect(
    "SELECT YEAR:",
    options=df['ON_YEAR'].unique(),
    default=df['ON_YEAR'].unique()
)


qtr = st.sidebar.multiselect(
    "SELECT QTR:",
    options=df['THE_QUARTER_TO_MATCH_AND_ANALYZE'].unique(),
    default=df['THE_QUARTER_TO_MATCH_AND_ANALYZE'].unique()
)


month = st.sidebar.multiselect(
    "SELECT MONTH:",
    options=df['ON_MONTH'].unique(),
    default=df['ON_MONTH'].unique()
    
)

ranking = st.sidebar.multiselect(
    "SELECT RANK:",
    options=df['RANKING'].unique(),
    default=df['RANKING'].unique()
)

store = st.sidebar.multiselect(
    "SELECT STORE:",
    options=df['STORE_TO_ANALYZE_AND_REPLICATE_MARKTING'].unique(),
    default=df['STORE_TO_ANALYZE_AND_REPLICATE_MARKTING'].unique()
)

df_selected = df.query(
    "RANKING == @ranking & ON_YEAR == @year & THE_QUARTER_TO_MATCH_AND_ANALYZE == @qtr & ON_MONTH == @month & STORE_TO_ANALYZE_AND_REPLICATE_MARKTING == @store"
)

# -- page title
st.title(":star: Moshe Khorshidi Home Task")
st.markdown("##")

# -- top boolets numbers
total_stock = df_selected['NEW_TARGET_RANGE_TOP_BOUNDARY'].sum()
avg_total_stock = round(df_selected['NEW_TARGET_RANGE_TOP_BOUNDARY'].mean(),2)
med_total_stock = round(df_selected['NEW_TARGET_RANGE_TOP_BOUNDARY'].median(),2)

left_column, center_column, right_column = st.columns(3)

with left_column:
    st.subheader(f"Total Stock: {total_stock:,}")
with center_column:
    st.subheader(f"Average Stock: {avg_total_stock:,}")
with right_column:
     st.subheader(f"Medien of Stock: {med_total_stock:,}")

st.write("---")
# see df on app
with st.expander("Data Preview"):
    st.dataframe(df_selected)

column_name_to_x_axis = st.selectbox('**Choose a X axis Column**',
                                    options = df_selected.columns.tolist())
column_name_to_y_axis = st.selectbox('**Choose a y axis Column**',
                                    options = df_selected.columns.tolist())

try: 
    
    with left_column:
        fig_bar = px.bar(df_selected,
        x = f'{column_name_to_x_axis}',
        y= f'{column_name_to_y_axis}',
        orientation="h",
        title="<b>My horizontal bar Vizz</b>",
        color_discrete_sequence = ["#008388"] * len(df_selected),
        template="plotly_white")

        st.plotly_chart(fig_bar)

    with right_column:

        fig_pie = px.pie(df_selected, values=f'{column_name_to_y_axis}', names=f'{column_name_to_x_axis}', title="<b>My pie Vizz</b>")

        st.plotly_chart(fig_pie)

except:

    st.info("**Set filters for visualization**", icon='📊')

