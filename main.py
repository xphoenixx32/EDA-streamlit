import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pygwalker.api.streamlit import StreamlitRenderer

st.set_page_config(
    page_title = 'Dashboard for EDA',
    layout = 'wide',
)
st.title('Dashboard for EDA')

uploaded_file = st.file_uploader(
        'Choose a CSV file', 
        type = 'csv',
    )

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader('Data Summary')
    st.dataframe(df)
    st.write(df.describe([.25,.75,.9,.95]))
    data_types = df.dtypes.to_frame('Types')
    st.write(data_types.sort_values('Types'))
    
    st.divider()

    st.subheader('Interactive Dashboard')

    @st.cache_resource
    def get_pyg_renderer() -> 'StreamlitRenderer':
        return StreamlitRenderer(df, spec = './gw_config.json')

    renderer = get_pyg_renderer()
    renderer.explorer()

    st.divider()

    st.subheader('Filter Data')
    columns = df.columns.tolist()
    selected_column = st.selectbox('Select column to filter by', columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox('Select value', unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    # st.subheader('Scatter Plot for Filtered Data')
    # x_column = st.selectbox('Select X-axis column', columns)
    # y_column = st.selectbox('Select Y-axis column', columns)

    # if st.button('Generate Plot'):
    #     st.scatter_chart(filtered_df.set_index(x_column)[y_column])
    
    st.divider()
else:
    st.write('Press "Browse Files" to Upload Data')
