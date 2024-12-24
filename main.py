import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pygwalker.api.streamlit import StreamlitRenderer
#------------------------------------------------------------------------------------------------------#

st.title("Exploratory Data Analysis Toolkit")
sns.set_theme(style = "whitegrid")
#------------------------------------------------------------------------------------------------------#

# Allow user to upload a file or choose a predefined dataset
st.subheader("👾 Choose a Dataset")
#------------------------------------------------------------------------------------------------------#

# Predefined dataset selection
dataset_options = ['healthexp',
                   'iris', 
                   'mpg',
                   'penguins', 
                   'taxis', 
                   'tips',
                   'titanic']

# Dataset summaries
dataset_summaries = {
    'healthexp': "Health expenditure dataset with data on health-related expenses and outcomes across various countries. Commonly used in health economics and policy analysis.",
    'iris': "Classic dataset containing measurements of sepal and petal lengths and widths for three species of Iris flowers (Setosa, Versicolor, Virginica). Frequently used for machine learning classification tasks.",
    'mpg': "Dataset about fuel efficiency of cars, with attributes such as miles per gallon (MPG), number of cylinders, horsepower, weight, model year, and origin. Often used for regression and exploratory data analysis.",
    'penguins': "Data on three species of penguins (Adelie, Chinstrap, Gentoo) including measurements like flipper length, bill dimensions, and body mass. A modern alternative to the iris dataset for classification tasks.",
    'taxis': "Dataset on taxi rides, including attributes like pickup and drop-off times, distances, fares, and tip amounts. Often used for time series and pricing analysis.",
    'tips': "Dataset containing information about tips given in a restaurant, with attributes like total bill, tip amount, gender, smoking status, and day of the week. Ideal for statistical and predictive analysis of tipping behavior.",
    'titanic': "Famous dataset on Titanic passengers, including attributes such as age, sex, class, survival status, and ticket price. Widely used for machine learning classification tasks and survival analysis."
}

# Dataset column descriptions
dataset_columns = {
    'healthexp': {
        'country': "Name of the country.",
        'year': "Year of observation.",
        'life_exp': "Average life expectancy in years.",
        'health_exp': "Health expenditure per capita in USD."
    },
    'iris': {
        'sepal_length': "Length of the sepal in cm.",
        'sepal_width': "Width of the sepal in cm.",
        'petal_length': "Length of the petal in cm.",
        'petal_width': "Width of the petal in cm.",
        'species': "Species of Iris (Setosa, Versicolor, Virginica)."
    },
    'mpg': {
        'mpg': "Miles per gallon, a measure of fuel efficiency.",
        'cylinders': "Number of cylinders in the car engine.",
        'displacement': "Engine displacement in cubic inches.",
        'horsepower': "Horsepower of the car.",
        'weight': "Weight of the car in pounds.",
        'acceleration': "Time to accelerate from 0 to 60 mph in seconds.",
        'model_year': "Year of the car's model (e.g., 70 for 1970).",
        'origin': "Origin of the car (1: USA, 2: Europe, 3: Japan).",
        'name': "Name of the car model."
    },
    'penguins': {
        'species': "Species of penguins (Adelie, Chinstrap, Gentoo).",
        'island': "Island where the penguin was observed.",
        'bill_length_mm': "Length of the penguin's bill in mm.",
        'bill_depth_mm': "Depth of the penguin's bill in mm.",
        'flipper_length_mm': "Length of the penguin's flipper in mm.",
        'body_mass_g': "Body mass of the penguin in grams.",
        'sex': "Sex of the penguin (male or female)."
    },
    'taxis': {
        'pickup_datetime': "Date and time of the pickup.",
        'dropoff_datetime': "Date and time of the drop-off.",
        'passenger_count': "Number of passengers in the taxi.",
        'trip_distance': "Distance of the trip in miles.",
        'fare_amount': "Fare amount in USD.",
        'tip_amount': "Tip amount given in USD.",
        'total_amount': "Total amount charged in USD.",
        'payment_type': "Payment method used (e.g., credit card, cash)."
    },
    'tips': {
        'total_bill': "Total bill amount in USD.",
        'tip': "Tip amount in USD.",
        'sex': "Sex of the customer (male or female).",
        'smoker': "Whether the customer is a smoker (yes or no).",
        'day': "Day of the week the transaction occurred.",
        'time': "Time of day (Lunch or Dinner).",
        'size': "Size of the dining party."
    },
    'titanic': {
        'survived': "Survival status (0: No, 1: Yes).",
        'pclass': "Passenger class (1: First, 2: Second, 3: Third).",
        'sex': "Sex of the passenger (male or female).",
        'age': "Age of the passenger in years.",
        'sibsp': "Number of siblings/spouses aboard.",
        'parch': "Number of parents/children aboard.",
        'fare': "Fare amount paid in USD.",
        'embarked': "Port of embarkation (C: Cherbourg, Q: Queenstown, S: Southampton).",
        'class': "Passenger class as a string (First, Second, Third).",
        'who': "Categorical description of who (man, woman, child).",
        'deck': "Deck of the ship the passenger was on.",
        'embark_town': "Town where the passenger embarked.",
        'alive': "Survival status as a string (yes or no).",
        'alone': "Whether the passenger was alone (True or False)."
    }
}

selected_dataset = st.selectbox(
    '🅰️ Select a Seaborn Dataset',
    ['None'] + dataset_options  # Add 'None' for default empty selection
)
#------------------------------------------------------------------------------------------------------#

uploaded_file = st.file_uploader(
    '🅱️ or Upload a CSV File',
    type = 'csv',
)
st.warning("CSV should Less than 100k rows", icon = "💀")
st.divider()
#------------------------------------------------------------------------------------------------------#

# Load the selected dataset or uploaded file
if selected_dataset != 'None':
    df = sns.load_dataset(selected_dataset)
    st.success(f"✅ Have Loaded <`{selected_dataset}`> dataset from Seaborn!")
    st.subheader("🪄 Brief Intro to this Data & Columns")
    st.info(dataset_summaries[selected_dataset], icon = "ℹ️")
    # Display column descriptions
    if selected_dataset in dataset_columns:
        for col, desc in dataset_columns[selected_dataset].items():
            st.markdown(f"**{col}**: {desc}")
elif uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ CSV file uploaded successfully!")
else:
    df = None
st.divider()
#------------------------------------------------------------------------------------------------------#

st.subheader("🎮 Switch Tabs for Different Purposes")
# Proceed only if a dataset is loaded
if df is not None:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['⎡ ¹🔍 Summary Info', 
                                                        '⎡ ²🔍 Filter & View', 
                                                        '⎡ ³📈 Violin & Area Plot', 
                                                        '⎡ ⁴📈 Density Plot', 
                                                        '⎡ ⁵📈 Corr Matrix',
                                                        '⎡ ⁶📈 Pair Plot', 
                                                        '⎡ ⛔ Interactive Dashboard'])
    #------------------------------------------------------------------------------------------------------#
    with tab1:
        st.warning(" Summary & Data types of the Dataset ", icon = "🕹️")
        st.info('Here is the Dataset', icon = "1️⃣")
        st.dataframe(df)
        
        st.divider()

        st.info('Data Type of Variables', icon = "2️⃣")
        # Data types overview
        data_types = df.dtypes.to_frame('Types')
        data_types['Types'] = data_types['Types'].astype(str)  # Convert to strings for sorting
        st.write(data_types.sort_values('Types'))
        
        st.divider()
      
        # Only describe numeric columns
        st.info('Statistic of Numeric Variables', icon = "3️⃣")
        numeric_df = df.select_dtypes(include = ['number'])
        if not numeric_df.empty:
            st.write(numeric_df.describe([.25, .75, .9, .95]))
        else:
            st.write("No numeric columns to describe.")
    #------------------------------------------------------------------------------------------------------#
    with tab2:
        st.warning(" Filter & View on Specific Column & Value ", icon="🕹️")
        # Filter Data Section
        columns = df.columns.tolist()

         # Unique keys for selectbox
        selected_column = st.selectbox(
            'Select column to filter by',
            columns,
            key = 'column_selector_tab2',
        )
    
        if selected_column:
            # Show Filtered Data
            unique_values = df[selected_column].dropna().unique()  # Drop NaNs for filtering
            unique_values = [str(value) for value in unique_values]  # Ensure all values are string
            selected_value = st.selectbox(
                'Select value',
                unique_values,
                key = 'value_selector_tab2',
            )

            st.divider()
            
            # Filter DataFrame
            st.info(f'Filtered Data of {selected_column} = {selected_value}', icon = "1️⃣")
            filtered_df = df[df[selected_column].astype(str) == selected_value]
            st.write("Filtered DataFrame:")
            st.write(filtered_df)
            
            st.divider()
            
            # Calculate Data Groupby Selected-Column
            st.info(f'Value Count Groupby {selected_column}', icon = "2️⃣")
            group_stats = df.groupby(selected_column).size().reset_index(name = 'counts')
            group_stats.set_index(selected_column, inplace = True)
            st.write(group_stats.sort_values('counts', ascending = False))
    #------------------------------------------------------------------------------------------------------#
    with tab3:
        st.warning(" Realize the Concentration of Data points ", icon = "🕹️")
        
        # Filter numeric and categorical columns
        numeric_columns = df.select_dtypes(include = ['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include = ['object', 'category']).columns.tolist()

        if numeric_columns and categorical_columns:
            # Allow user to select a categorical column and a numeric column
            selected_category_column = st.selectbox(
              'Select Categorical Column',
              categorical_columns,
              key = 'category_selector_tab3',
            )
            selected_numeric_column = st.selectbox(
              'Select Numeric Column',
              numeric_columns,
              key = 'numeric_selector_tab3',
            )

            st.divider()

            if selected_category_column and selected_numeric_column:
                # #1 Violin plot
                st.info(f'Violin plot of {selected_numeric_column} by {selected_category_column}', icon = "ℹ️")
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

                # Calculate Statistics
                grouped_stats = df.groupby(selected_category_column)[selected_numeric_column].agg(
                    count = 'count',
                    mean = 'mean',
                    std = 'std',
                    q1 = lambda x: x.quantile(0.25),
                    median = 'median',
                    q3 = lambda x: x.quantile(0.75),
                ).reset_index()

                grouped_stats[['mean', 'std', 'q1', 'median', 'q3']] = grouped_stats[['mean', 'std', 'q1', 'median', 'q3']].round(3)
              
                # Rename Columns of Statistics
                grouped_stats.rename(
                    columns = {
                        'count': 'Count',
                        'mean': 'Mean',
                        'std': 'STD',
                        'q1': 'Q1',
                        'median': 'Q2',
                        'q3': 'Q3',
                    },
                    inplace = True,
                )
                grouped_stats.set_index(selected_category_column, inplace = True)
                
                st.info(f'Statistical Summary of {selected_numeric_column} grouped by {selected_category_column}', icon = "📊")
                st.write(grouped_stats.T)
                
                st.divider()

                # #2 Displot
                st.info(f'Area Distribution of {selected_numeric_column} by {selected_category_column}', icon = "ℹ️")
                sns_displot = sns.displot(
                    data = df,
                    x = selected_numeric_column,
                    hue = selected_category_column,
                    kind = "kde",
                    height = 6,
                    aspect = 1.5, # ratio of width:height = aspect
                    multiple = "fill",
                    clip = (0, None),
                    palette = "ch:rot = -.25, hue = 1, light = .75",
                )

                st.pyplot(sns_displot.fig)
        else:
            st.write("Ensure your dataset contains both numeric and categorical columns.", icon = "❗")
    #------------------------------------------------------------------------------------------------------#
    with tab4:
        st.warning(" Brief Realization on Correlation by Categorical Var Between Numeric Var ", icon = "🕹️")
        
        # Filter numeric columns
        numeric_columns = df.select_dtypes(include = ['number']).columns.tolist()

        # Filter categorical columns
        categorical_columns = df.select_dtypes(include = ['object', 'category']).columns.tolist()

        if numeric_columns and categorical_columns:
            # Allow user to select a categorical column
            selected_category_column = st.selectbox(
              'Select Categorical Column',
              categorical_columns,
              key = 'category_selector_tab4',
            )
            unique_category_values = df[selected_category_column].unique().tolist()

            # Allow user to select numeric columns for X and Y axes
            st.info(" X & Y Should be Different ", icon = "ℹ️")
            selected_x = st.selectbox(
              'Select X-axis column',
              numeric_columns,
              key = 'x_axis_selector_tab4',
            )
            selected_y = st.selectbox(
              'Select Y-axis column',
              numeric_columns,
              key = 'y_axis_selector_tab4',
            )
            if selected_x and selected_y:
                # Create subplots based on the number of unique category values
                num_categories = len(unique_category_values)
                cols = 2  # Maximum 2 plots per row
                rows = (num_categories + cols - 1) // cols  # Calculate rows needed

                # Initialize the figure
                fig, axes = plt.subplots(
                  rows, cols,
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
                        cmap = "Greens",
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
        st.warning("Correlation Matrix between Numeric Variables", icon="🕹️")
        
        # Filter numeric columns
        numeric_columns = df.select_dtypes(include = ['number']).columns.tolist()
        
        if numeric_columns:
            # Put Numeric Var into Multi-Select
            selected_columns = st.multiselect(
                "Select numeric columns for Corr Matrix:",
                numeric_columns,
                default = numeric_columns,  # default settings for select all numeric
            )
            
            if selected_columns:
                # Compute correlation matrix
                correlation_matrix = df[selected_columns].corr()
    
                # Mask to hide the upper triangle
                mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    
                # Plot the heatmap
                fig, ax = plt.subplots(figsize = (12, 12))
                sns.heatmap(
                    correlation_matrix,
                    mask = mask,  # Apply the mask to hide the upper triangle
                    annot = True,
                    cmap = "coolwarm",
                    fmt = ".2f",
                    ax = ax,
                )
                ax.set_title("Correlation Matrix Heatmap (Lower Triangle Only)")
                
                # 在 Streamlit 中顯示熱力圖
                st.pyplot(fig)
            else:
                st.warning("No columns selected. Please select at least one numeric column.", icon = "⚠️")
        else:
            st.error("Your dataset does not contain any numeric columns.", icon="❗")
    #------------------------------------------------------------------------------------------------------#
    with tab6:
        st.warning(" Comparison between Numeric Var GroupBy Categorical Var  ", icon = "🕹️")
        
        # Filter numeric and categorical columns
        numeric_columns = df.select_dtypes(include = ['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include = ['object', 'category']).columns.tolist()

        if numeric_columns and categorical_columns:
            selected_category_column = st.selectbox(
              'Select Categorical Column',
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
                    pairplot_fig = sns.pairplot(
                      df,
                      hue = selected_category_column,
                      vars = numeric_columns,
                      corner = True,
                      plot_kws = {'alpha': 0.7},
                    )
                    
                    # Display the plot using Streamlit
                    st.pyplot(pairplot_fig)
        else:
            st.write("Ensure your dataset contains both numeric and categorical columns.", icon = "❗")
    #------------------------------------------------------------------------------------------------------#
    with tab7:
        st.warning(" This Tab can only be used by the Developer ", icon = "⛔")
        st.warning(" Remember to [Clear Cache] ", icon = "✂️")
        st.info(" Switch [Settings] ➡️ [Appearance] ➡️ [Wide Mode] ", icon = "ℹ️")
        @st.cache_resource
        def get_pyg_renderer() -> 'StreamlitRenderer':
            return StreamlitRenderer(
              df, 
              spec='./gw_config.json', 
              spec_io_mode = 'rw',
            )

        renderer = get_pyg_renderer()
        renderer.explorer()
    #------------------------------------------------------------------------------------------------------#
else:
    st.error('🅰️ Select a Seaborn Dataset 🅱️ or Upload a CSV File to GET STARTED', icon = "📎")
