import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import datetime
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Superstore!!!", page_icon="bar_chart:", layout="wide")

st.title(" :bar_chart: Sample Super Store EDA")
st.markdown ('<style> div.block-container {padding-top:1rem;}</style>', unsafe_allow_html=True)

f1 = st.file_uploader(" :file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if f1 is not None:
    filename = f1.name 
    st.write(filename)
    df= pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"C:\Users\vaish\Desktop\Project\streamlit")
    df = pd.read_csv("Superstore.csv", encoding = "ISO-8859-1")

col1, col2 = st.columns((2))
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
start_date = st.date_input('Start date', today)
end_date = st.date_input('End date', tomorrow)
if start_date < end_date:
    st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.error('Error: End date must fall after start date.')



st.sidebar.header("Choose your filter: ")
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]


state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
if not state:
    df3=df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]


city = st.sidebar.multiselect("Pick the City", df["City"].unique())


if not region and not state and not city:
    filtere_df = df
elif not state and not city:
    filtere_df = df[df["Region"].isin(region)]
elif not region and not city:
    fitere_df = df[df["State"].isin(state)]

elif state and city:
    filtere_df =df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtere_df =df3[df["State"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtere_df =df3[df["State"].isin(region) & df3["City"].isin(state)]
elif city:
    filtere_df = df3[df3["City"].isin(city)]
else:
    filtere_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

category_df =filtere_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()

with col1:
    st.subheader("Category wise Sales")
    fig = px.bar(category_df, x = "Category", y ="Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                template="seaborn")
    st.plotly_chart(fig,use_container_width = True, height = 200)

with col2:
    st.subheader("Region wise Sales")
    fig = px.pie(filtere_df, values = "Sales", names = "Region", hole = 0.5)
    fig.update_traces(text = filtere_df["Region"], textposition ="outside")
    st.plotly_chart(fig, use_container_width=True )

cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Category_Viewdata"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = region.to_csv(index=False).encode('utf-8')

        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')
        
with cl2:
    with st.expander("Region_Viewdata"):
        region = filtere_df.groupby(by = "Region", as_index = False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')
        

st.subheader("Hierarchical view of sales using TreeMap")
fig3 = px.treemap(filtere_df, path = ["Region","Category","Sub-Category"], values = "Sales", hover_data=["Sales"],color="Sub-Category")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment wise Sales')
    fig = px.pie(filtere_df, values = "Sales", names = "Segment", template= "plotly_dark")
    fig.update_traces(text= filtere_df["Segment"], textposition = "inside")
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader('Category wise Sales')
    fig = px.pie(filtere_df, values = "Sales", names = "Category", template= "gridon")
    fig.update_traces(text= filtere_df["Category"], textposition = "inside")
    st.plotly_chart(fig, use_container_width=True)



data1 = px.scatter(filtere_df, x="Sales", y="Profit", size="Quantity")
data1['layout'].update(title="Relationship between sales and Profits using Scatter Plot.",
                       titlefont=dict(size=20), xaxis = dict(title="Sales", titlefont=dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(data1, use_container_width=True)


with st.expander("View Data"):
    st.write(filtere_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))


csv=df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data=csv, file_name = "Data.csv", mime="text/csv")

