import streamlit as st
import pandas as pd
import plotly.express as px
import random

# --- Data Loading and Preparation ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], format='%d-%m-%Y')
        df['Year'] = df['Invoice Date'].dt.year.astype(str)
        df['Month'] = df['Invoice Date'].dt.month.astype(str).str.zfill(2)
        return df
    except FileNotFoundError:
        st.error(f"Could not find {file_path}.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

st.title("Sales Register Analysis (with SA 520 Procedures)")

# --- File Upload ---
st.sidebar.header("Data Upload")
current_year_file = st.sidebar.file_uploader("Upload Current Year Sales Register (CSV)", type=["csv"])
prior_year_file = st.sidebar.file_uploader("Upload Prior Year Sales Register (CSV)", type=["csv"])

current_year_df = None
prior_year_df = None
current_year_filtered_df = None
prior_year_filtered_df = None

if current_year_file:
    current_year_df = load_data(current_year_file)
if prior_year_file:
    prior_year_df = load_data(prior_year_file)

# --- Filtering ---
st.sidebar.header("Filters")

if current_year_df is not None:
    start_date = st.sidebar.date_input("Start Date", current_year_df['Invoice Date'].min())
    end_date = st.sidebar.date_input("End Date", current_year_df['Invoice Date'].max())
    selected_customer = st.sidebar.selectbox("Customer", ["All"] + list(current_year_df['Customer Name'].unique()))
    min_amount = st.sidebar.number_input("Minimum Amount", value=0.0)
    max_amount = st.sidebar.number_input("Maximum Amount", value=float(current_year_df['Total Amount'].max()))

    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)

    current_year_filtered_df = current_year_df[
        (current_year_df['Invoice Date'] >= start_date) &
        (current_year_df['Invoice Date'] <= end_date)
    ]
    if selected_customer != "All":
        current_year_filtered_df = current_year_filtered_df[current_year_filtered_df['Customer Name'] == selected_customer]
    current_year_filtered_df = current_year_filtered_df[
        (current_year_filtered_df['Total Amount'] >= min_amount) &
        (current_year_filtered_df['Total Amount'] <= max_amount)
    ]

    if prior_year_df is not None:
        prior_year_filtered_df = prior_year_df[
            (prior_year_df['Invoice Date'] >= start_date) &
            (prior_year_df['Invoice Date'] <= end_date)
        ]
        if selected_customer != "All":
            prior_year_filtered_df = prior_year_filtered_df[prior_year_filtered_df['Customer Name'] == selected_customer]
        prior_year_filtered_df = prior_year_filtered_df[
            (prior_year_filtered_df['Total Amount'] >= min_amount) &
            (prior_year_filtered_df['Total Amount'] <= max_amount)
        ]

    st.subheader("Filtered Current Year Data")
    st.dataframe(current_year_filtered_df)

    if prior_year_df is not None:
        st.subheader("Filtered Prior Year Data")
        st.dataframe(prior_year_filtered_df)

# --- Trend Analysis ---
    if prior_year_filtered_df is not None and current_year_filtered_df is not None:
        st.header("Trend Analysis")

        current_year_monthly = current_year_filtered_df.groupby(['Month', 'Year'])['Total Amount (Inc. Tax)'].sum().reset_index()
        prior_year_monthly = prior_year_filtered_df.groupby(['Month', 'Year'])['Total Amount (Inc. Tax)'].sum().reset_index()

        if current_year_monthly.empty or prior_year_monthly.empty:
            st.warning("No data available for trend analysis after filtering.")
        else:
            all_months_df = pd.DataFrame({'Month': [str(i).zfill(2) for i in range(1, 13)]})
            current_year_monthly = pd.merge(all_months_df, current_year_monthly, on='Month', how='left')
            prior_year_monthly = pd.merge(all_months_df, prior_year_monthly, on='Month', how='left')
            current_year_monthly.fillna(0, inplace=True)
            prior_year_monthly.fillna(0, inplace=True)
            merged_monthly = pd.merge(current_year_monthly, prior_year_monthly, on='Month', suffixes=('_Current', '_Prior'), how='outer')
            merged_monthly.fillna(0, inplace=True)
            merged_monthly['Percentage Change'] = ((merged_monthly['Total Amount (Inc. Tax)_Current'] - merged_monthly['Total Amount (Inc. Tax)_Prior']) / merged_monthly['Total Amount (Inc. Tax)_Prior']) * 100
            merged_monthly['Percentage Change'].fillna(0, inplace=True)

            st.subheader("Monthly Sales Comparison")
            merged_monthly['Total Amount (Inc. Tax)_Current'] = merged_monthly['Total Amount (Inc. Tax)_Current'].apply(lambda x: f'₹{x:,.2f}')
            merged_monthly['Total Amount (Inc. Tax)_Prior'] = merged_monthly['Total Amount (Inc. Tax)_Prior'].apply(lambda x: f'₹{x:,.2f}')
            st.dataframe(merged_monthly)

            plot_data = pd.concat([
                current_year_monthly.assign(Year=current_year_monthly['Year']),
                prior_year_monthly.assign(Year=prior_year_monthly['Year'])
            ])

            fig = px.line(plot_data, x='Month', y='Total Amount (Inc. Tax)', color='Year',
                          title='Monthly Sales Trend')
            st.plotly_chart(fig)

            st.subheader("Significant Changes ( > 10% )")
            significant_changes = merged_monthly[abs(merged_monthly['Percentage Change']) > 10]
            st.dataframe(significant_changes.style.applymap(lambda x: 'background-color : yellow' if abs(x) > 10 else '', subset=['Percentage Change']))

# --- Sample Selection ---
    st.header("Sample Selection")

    if current_year_filtered_df is not None:
        sampling_method = st.selectbox("Initial Sampling Method", ["Random", "Systematic", "Monetary Unit Sampling", "Judgmental", "Stratified"])
        sample_size = st.number_input("Initial Sample Size", min_value=1, max_value=len(current_year_filtered_df), value=min(10, len(current_year_filtered_df)))

        initial_sample = None
        initial_methodology_text = ""
        final_sample = None  # Initialize final_sample
        methodology_text = ""

        # --- Initial Sample Generation ---
        if sampling_method == "Random":
            if st.button("Generate Initial Random Sample"):
                initial_sample = current_year_filtered_df.sample(n=sample_size)
                initial_methodology_text = f"**Random Sampling:** A random sample of {sample_size} transactions was selected."
                final_sample = initial_sample  # Set final_sample here
                methodology_text = initial_methodology_text

        elif sampling_method == "Systematic":
            if st.button("Generate Initial Systematic Sample"):
                start = st.number_input("Starting Point", min_value=1, max_value=len(current_year_filtered_df), value=1)
                step = len(current_year_filtered_df) // sample_size
                if step > 0:
                    initial_sample = current_year_filtered_df.iloc[start-1::step]
                    initial_methodology_text = f"**Systematic Sampling:** A systematic sample of {sample_size} transactions was selected, starting from item {start} and selecting every {step}th item."
                    final_sample = initial_sample  # Set final_sample here
                    methodology_text = initial_methodology_text
                else:
                    st.warning("Sample size is too large for systematic sampling.")

        elif sampling_method == "Monetary Unit Sampling":
            if st.button("Generate Initial MUS Sample"):
                current_year_filtered_df['Cumulative Total'] = current_year_filtered_df['Total Amount (Inc. Tax)'].cumsum()
                total_amount = current_year_filtered_df['Cumulative Total'].iloc[-1]
                if total_amount > 0:
                    interval = total_amount / sample_size
                    sample_indices = []
                    for i in range(sample_size):
                        random_amount = random.uniform(i * interval, (i + 1) * interval)
                        selected_index = current_year_filtered_df[current_year_filtered_df['Cumulative Total'] >= random_amount].index[0]
                        if selected_index not in sample_indices:
                            sample_indices.append(selected_index)
                    initial_sample = current_year_filtered_df.loc[sample_indices]
                    initial_methodology_text = f"**Monetary Unit Sampling (MUS):** An MUS sample of {sample_size} transactions was selected.  The sampling interval was ₹{interval:,.2f}."
                    final_sample = initial_sample  # Set final_sample here
                    methodology_text = initial_methodology_text
                else:
                    st.warning("Total amount is zero. Cannot perform MUS.")
                current_year_filtered_df = current_year_filtered_df.drop(columns=['Cumulative Total'], errors='ignore')

        elif sampling_method == "Judgmental":
            st.write("Select rows directly from the filtered data table above for the initial sample.")
            initial_selected_rows = st.multiselect("Select Initial Invoice Numbers", current_year_filtered_df['Invoice Number'].tolist(), key="initial_selection")
            if st.button("Generate Initial Judgmental Sample"):
                initial_sample = current_year_filtered_df[current_year_filtered_df['Invoice Number'].isin(initial_selected_rows)]
                initial_methodology_text = f"**Judgmental Sampling:** The following invoice numbers were initially selected: {', '.join(initial_selected_rows)}"
                final_sample = initial_sample  # Set final_sample here
                methodology_text = initial_methodology_text

        elif sampling_method == "Stratified":
            st.write("Define strata based on 'Total Amount (Inc. Tax)'")
            strata_boundaries = st.text_input("Enter strata boundaries, separated by commas (e.g., 1000,5000,10000)", "1000,5000")
            if st.button("Generate Initial Stratified Sample"):
                try:
                    boundaries = [float(x.strip()) for x in strata_boundaries.split(',')]
                    boundaries = [0] + boundaries + [float('inf')]
                    strata_labels = [f"{boundaries[i]}-{boundaries[i+1]}" for i in range(len(boundaries) - 1)]
                    current_year_filtered_df['Stratum'] = pd.cut(current_year_filtered_df['Total Amount (Inc. Tax)'], bins=boundaries, labels=strata_labels, include_lowest=True)
                    initial_sample = current_year_filtered_df.groupby('Stratum', group_keys=False).apply(lambda x: x.sample(min(len(x), sample_size // len(strata_labels))))
                    initial_methodology_text = f"**Stratified Sampling:** The data was stratified based on 'Total Amount (Inc. Tax)' with boundaries: {strata_boundaries}.  A sample of size {sample_size} was selected proportionally."
                    final_sample = initial_sample  # Set final_sample here
                    methodology_text = initial_methodology_text
                except Exception as e:
                    st.error(f"Error in stratified sampling: {e}")
                current_year_filtered_df = current_year_filtered_df.drop(columns=['Stratum'], errors='ignore')

        # --- Add Judgmental Sample (Optional) ---
        st.subheader("Add Judgmental Sample (Optional)")
        st.write("Select additional rows to add to the sample, if needed.")
        additional_selected_rows = st.multiselect("Select Additional Invoice Numbers", current_year_filtered_df['Invoice Number'].tolist(), key="additional_selection")
        if st.button("Add to Sample"):
            additional_sample = current_year_filtered_df[current_year_filtered_df['Invoice Number'].isin(additional_selected_rows)]

            # Combine samples correctly
            if initial_sample is not None:  # If initial exists, combine
                final_sample = pd.concat([initial_sample, additional_sample]).drop_duplicates(subset=['Invoice Number'])
                methodology_text = f"{initial_methodology_text}  \n\n**Additional Judgmental Selections:** The following invoice numbers were added: {', '.join(additional_selected_rows)}"
            else: #if no initial selection
                final_sample = additional_sample
                methodology_text = f"**Judgmental Sampling:** The following invoice numbers were selected: {', '.join(additional_selected_rows)}"

        # --- Display Results ---
        if final_sample is not None:
            st.subheader("Final Sample")
            st.dataframe(final_sample)
            st.write(methodology_text)

    else:
        st.warning("Please upload and filter the current year's data.")
