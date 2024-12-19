import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pygwalker.api.streamlit import StreamlitRenderer
#------------------------------------------------------------------------------------------------------#

st.title('EDA Toolkit')
sns.set_theme(style = "whitegrid")
#------------------------------------------------------------------------------------------------------#

# Allow user to upload a file or choose a predefined dataset
st.subheader("Upload or Select a Dataset")

uploaded_file = st.file_uploader(
    ' 1️⃣ Upload a CSV file 🔻 ',
    type = 'csv',
)
#------------------------------------------------------------------------------------------------------#

# Predefined dataset selection
dataset_options = ['penguins', 
                   'titanic', 
                   'diamonds', 
                   'iris', 
                   'tips']
selected_dataset = st.selectbox(
    ' 2️⃣ or Select a Dataset Below 🔻 ',
    ['None'] + dataset_options  # Add 'None' for default empty selection
)
#------------------------------------------------------------------------------------------------------#

# Load the selected dataset or uploaded file
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV file uploaded successfully!")
elif selected_dataset != 'None':
    df = sns.load_dataset(selected_dataset)
    st.success(f"Loaded `{selected_dataset}` dataset from seaborn.")
else:
    df = None
#------------------------------------------------------------------------------------------------------#

# Proceed only if a dataset is loaded
if df is not None:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([' 🔍 Summary Info ', 
                                                        ' 🔍 Filter & View ', 
                                                        ' 📊 Violin & Area Plot ', 
                                                        ' 📊 Cross-Density Plot ', 
                                                        ' 📊 Correlation Matrix ',
                                                        ' 📊 Pair Plot ', 
                                                        ' ⛔ Interactive Dashboard '])
    #------------------------------------------------------------------------------------------------------#
    with tab1:
        st.warning(" Summary & Data types of the Dataset ")
        st.dataframe(df)
        
        st.divider()
        
        # Only describe numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            st.write(numeric_df.describe([.25, .75, .9, .95]))
        else:
            st.write("No numeric columns to describe.")
        
        st.divider()
        
        # Data types overview
        data_types = df.dtypes.to_frame('Types')
        data_types['Types'] = data_types['Types'].astype(str)  # Convert to strings for sorting
        st.write(data_types.sort_values('Types'))
    #------------------------------------------------------------------------------------------------------#
    with tab2:
        st.warning(" Filter & View on Specific Column & Value ")
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
    #------------------------------------------------------------------------------------------------------#
    with tab3:
        st.warning(" Realize the Concentration of Data points ")
        
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

            st.divider()

            if selected_category_column and selected_numeric_column:
                # #1 Violin plot
                st.subheader(f'Violin plot of {selected_numeric_column} by {selected_category_column}')

                fig, ax = plt.subplots(figsize = (12, 6))
                sns.violinplot(
                    data = df,
                    x = selected_category_column,
                    y = selected_numeric_column,
                    palette = "muted",
                    ax = ax,
                )
                ax.set_xlabel(selected_category_column)
                ax.set_ylabel(selected_numeric_column)
                
                st.pyplot(fig)
                
                st.divider()

                # #2 Displot
                st.subheader(f'Area Distribution of {selected_numeric_column} by {selected_category_column}')
                
                sns_displot = sns.displot(
                    data = df,
                    x = selected_numeric_column,
                    hue = selected_category_column,
                    kind = "kde",
                    height = 6,
                    multiple = "fill",
                    clip = (0, None),
                    palette = "ch:rot = -.25, hue = 1, light = .75",
                )

                st.pyplot(sns_displot.fig)
        else:
            st.write("Ensure your dataset contains both numeric and categorical columns.")
    #------------------------------------------------------------------------------------------------------#
    with tab4:
        st.warning(" Brief Realization on Cross-Correlation Between Numeric Var ")
        
        # Filter numeric columns
        numeric_columns = df.select_dtypes(include = ['number']).columns.tolist()

        # Filter categorical columns
        categorical_columns = df.select_dtypes(include = ['object', 'category']).columns.tolist()

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

                # Hide unused subplots
                for i in range(num_categories, len(axes)):
                    axes[i].axis('off')
                # Display the plot
                st.pyplot(fig)
    #------------------------------------------------------------------------------------------------------#
    with tab5:
        st.warning(" Correlation Matrix between Numeric Var ")
        
        # Filter numeric columns
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_columns:
            st.write("Numeric columns detected:", numeric_columns)
            
            # Compute correlation matrix
            correlation_matrix = df[numeric_columns].corr()

            # Mask to hide the upper triangle
            mask = np.triu(np.ones_like(correlation_matrix, dtype = bool))

            # Plot the heatmap
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(
                correlation_matrix,
                mask = mask,  # Apply the mask to hide the upper triangle
                annot = True,
                cmap = "coolwarm",
                fmt = ".2f",
                ax = ax
            )
            ax.set_title("Correlation Matrix Heatmap (Lower Triangle Only)")
            
            # Display the plot
            st.pyplot(fig)
        else:
            st.write("Ensure your dataset contains both numeric and categorical columns.")
    #------------------------------------------------------------------------------------------------------#
    with tab6:
        st.warning(" Comparison between Numeric Var GroupBy Categorical Var  ")
        
        # Filter numeric and categorical columns
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

        if numeric_columns and categorical_columns:
            selected_category_column = st.selectbox('Select Categorical Column',
                                                    categorical_columns,
                                                    key = 'category_selector_tab6',
                                                    )

            if selected_category_column:
                st.write(f"Selected Category: {selected_category_column}")

                # Check if selected columns exist in df
                if selected_category_column not in df.columns:
                    st.error(f"Column {selected_category_column} not found in dataframe.")
                else:
                    # Generate pairplot
                    pairplot_fig = sns.pairplot(df,
                                                hue = selected_category_column,
                                                vars = numeric_columns,
                                                corner = True,
                                                plot_kws = {'alpha': 0.7},
                                               )
                    
                    # Display the plot using Streamlit
                    st.pyplot(pairplot_fig)
        else:
            st.write("Ensure your dataset contains both numeric and categorical columns.")
    #------------------------------------------------------------------------------------------------------#
    with tab7:
        st.warning(" ⛔ Can only be used by the Developer ")
        @st.cache_resource
        def get_pyg_renderer() -> 'StreamlitRenderer':
            return StreamlitRenderer(df, 
                                     spec='./gw_config.json', 
                                     spec_io_mode = 'rw',
                                    )

        renderer = get_pyg_renderer()
        renderer.explorer()
    #------------------------------------------------------------------------------------------------------#
else:
    st.write('Press "Browse Files" to Upload Data or Select a Dataset')
