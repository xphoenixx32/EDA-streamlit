import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pygwalker.api.streamlit import StreamlitRenderer
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(
    page_title = 'Dashboard for EDA',
    layout = 'wide',
)
st.title('Dashboard for EDA')

tab1, tab2, tab3 = st.tabs(['[A] Data Summary', '[B] Filter Data Viewer', '[C] Interactive Dashbaord'])

uploaded_file = st.file_uploader(
        'Choose a CSV file', 
        type = 'csv',
    )

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    with tab1:
        # st.subheader('Data Summary')
        st.dataframe(df)
        
        data_summary = df.describe([.25,.75,.9,.95])
        data_types = df.dtypes.to_frame('Types')
        
        st.write(data_summary, data_types.sort_values('Types'))
        
        st.divider()
    with tab2:
        # st.subheader('Filter Data')
        columns = df.columns.tolist()
        selected_column = st.selectbox('Select column to filter by', columns)
        
        unique_values = df[selected_column].unique()
        selected_value = st.selectbox('Select value', unique_values)
        
        filtered_df = df[df[selected_column] == selected_value]
        
        st.write(filtered_df)
        
        st.divider()
    with tab3:
        # st.subheader('Interactive Dashboard')
        @st.cache_resource
        def get_pyg_renderer() -> 'StreamlitRenderer':
            return StreamlitRenderer(df, spec = './gw_config.json', spec_io_mode = 'rw')

        renderer = get_pyg_renderer()
        renderer.explorer()

        st.divider()
else:
    st.write('Press "Browse Files" to Upload Data')
