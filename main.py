import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from pygwalker.api.streamlit import StreamlitRenderer

st.title('EDA Toolkit')

sns.set_theme(style = "whitegrid")

# Allow user to upload a file or choose a predefined dataset
st.subheader("Upload or Select a Dataset")

uploaded_file = st.file_uploader(
    'Choose a CSV file',
    type = 'csv',
)

# Predefined dataset selection
dataset_options = ['diamonds', 'iris', 'tips', 'penguins', 'titanic']
selected_dataset = st.selectbox(
    'Or select a dataset from the list below:',
    ['None'] + dataset_options  # Add 'None' for default empty selection
)

# Load the selected dataset or uploaded file
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV file uploaded successfully!")
elif selected_dataset != 'None':
    df = sns.load_dataset(selected_dataset)
    st.success(f"Loaded `{selected_dataset}` dataset from seaborn.")
else:
    df = None
    st.warning("No dataset loaded. Please upload a file or select a dataset.")

# Proceed only if a dataset is loaded
if df is not None:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Summary', 
                                            'Filter Viewer', 
                                            '1-D Plot', 
                                            '2-D Plot', 
                                            'Interactive Dashboard'])

    ###################################################
    with tab1:
        st.dataframe(df)
        
        # Only describe numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            st.write(numeric_df.describe([.25, .75, .9, .95]))
        else:
            st.write("No numeric columns to describe.")

        # Data types overview
        data_types = df.dtypes.to_frame('Types')
        data_types['Types'] = data_types['Types'].astype(str)  # Convert to strings for sorting
        st.write(data_types.sort_values('Types'))

        st.divider()
    ###################################################
    with tab2:
        # Filter Data Section
        columns = df.columns.tolist()

        # Unique keys for selectbox
        selected_column = st.selectbox('Select column to filter by',
                                       columns,
                                       key = 'column_selector_tab2',
                                       )
        unique_values = df[selected_column].dropna().unique()  # Drop NaNs for filtering
        unique_values = [str(value) for value in unique_values]  # Ensure all values are string
        selected_value = st.selectbox('Select value',
                                      unique_values,
                                      key = 'value_selector_tab2',
                                      )

        # Filter DataFrame
        filtered_df = df[df[selected_column].astype(str) == selected_value]
        st.write(filtered_df)
    ###################################################
    with tab3:
        # Filter numeric and categorical columns
        numeric_columns = df.select_dtypes(include = ['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include = ['object', 'category']).columns.tolist()

        if numeric_columns and categorical_columns:
            # Allow user to select a categorical column and a numeric column
            selected_category_column = st.selectbox('Select Categorical Column', 
                                                    categorical_columns, 
                                                    key = 'category_selector_tab3',
                                                    )
            selected_numeric_column = st.selectbox('Select Numeric Column', 
                                                   numeric_columns, 
                                                   key = 'numeric_selector_tab3',
                                                   )

            if selected_category_column and selected_numeric_column:
                # Plot violin plot
                st.write(f'Violin plot of {selected_numeric_column} grouped by {selected_category_column}')

                fig, ax = plt.subplots(figsize=(12, 6))
                sns.violinplot(
                    data = df,
                    x = selected_category_column,
                    y = selected_numeric_column,
                    palette = "muted",
                    ax = ax,
                )
                ax.set_title(f'Violin Plot of {selected_numeric_column} by {selected_category_column}')
                ax.set_xlabel(selected_category_column)
                ax.set_ylabel(selected_numeric_column)

                # Display the plot
                st.pyplot(fig)
        else:
            st.write("Ensure your dataset contains both numeric and categorical columns.")
    ###################################################
    with tab4:
        # Filter numeric columns
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

        # Filter categorical columns
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

        if numeric_columns and categorical_columns:
            # Allow user to select a categorical column
            selected_category_column = st.selectbox('Select Categorical Column',
                                                    categorical_columns,
                                                    key = 'category_selector_tab4',
                                                    )
            unique_category_values = df[selected_category_column].unique().tolist()

            # Allow user to select numeric columns for X and Y axes
            selected_x = st.selectbox('Select X-axis column',
                                      numeric_columns,
                                      key = 'x_axis_selector_tab4',
                                      )
            selected_y = st.selectbox('Select Y-axis column',
                                      numeric_columns,
                                      key = 'y_axis_selector_tab4',
                                      )

            if selected_x and selected_y:
                # Create subplots based on the number of unique category values
                num_categories = len(unique_category_values)
                cols = 2  # Maximum 2 plots per row
                rows = (num_categories + cols - 1) // cols  # Calculate rows needed

                # Initialize the figure
                fig, axes = plt.subplots(rows, cols,
                                         figsize = (12, 6 * rows),
                                         constrained_layout = True,
                                         )
                axes = axes.flatten()  # Flatten axes for easy iteration

                # Plot each category
                for i, category in enumerate(unique_category_values):
                    ax = axes[i]
                    filtered_data = df[df[selected_category_column] == category]
                    
                    # Check if filtered data has sufficient variance
                    if len(filtered_data[selected_x].unique()) > 1 and len(filtered_data[selected_y].unique()) > 1:
                        sns.kdeplot(
                            data = filtered_data,
                            x = selected_x,
                            y = selected_y,
                            fill = True,
                            cmap = "Blues",
                            ax = ax,
                            warn_singular = False  # Suppress singular warnings
                        )
                        ax.set_title(f'{selected_category_column}: {category}')
                        ax.set_xlabel(selected_x)
                        ax.set_ylabel(selected_y)
                    else:
                        ax.text(0.5, 0.5, 
                                'Insufficient Data', 
                                fontsize = 12, 
                                ha = 'center', 
                                va = 'center',
                               )
                        ax.set_title(f'{selected_category_column}: {category}')
                        ax.axis('off')

                # Hide unused subplots
                for i in range(num_categories, len(axes)):
                    axes[i].axis('off')
                
                # Display the plot
                st.pyplot(fig)
    ###################################################
    with tab5:
        st.warning(" 1️⃣ Go to [Settings] > [Appearance] > Turn On [Wide Mode] ")
        st.warning(" 2️⃣ Go to [Developer options] > [Clear cache] ")
        @st.cache_resource
        def get_pyg_renderer() -> 'StreamlitRenderer':
            return StreamlitRenderer(df, 
                                     spec='./gw_config.json', 
                                     spec_io_mode = 'rw',
                                    )

        renderer = get_pyg_renderer()
        renderer.explorer()
    ###################################################
else:
    st.write('Press "Browse Files" to Upload Data or Select a Dataset')
