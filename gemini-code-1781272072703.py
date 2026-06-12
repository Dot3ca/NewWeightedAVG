import pandas as pd

def calculate_average_cost(input_file, output_file):
    try:
        # Load the spreadsheet
        # header=0 assumes the first row contains your column titles
        df = pd.read_excel(input_file, header=0)

        # Select columns by index (D=3, F=5, H=7, K=10)
        # We create a new dataframe with only the data we need
        data = df.iloc[:, [3, 5, 7, 10]].copy()
        
        # Rename columns to make them easier to reference
        data.columns = ['Stock_Code', 'Description', 'Quantity', 'Unit_Cost']

        # Calculate the total value per line item (Quantity * Cost)
        data['Total_Value'] = data['Quantity'] * data['Unit_Cost']

        # Group by Stock Code and Description, then sum up Quantity and Total Value
        grouped = data.groupby(['Stock_Code', 'Description']).agg({
            'Quantity': 'sum',
            'Total_Value': 'sum'
        }).reset_index()

        # Calculate the Weighted Average Cost
        # We use a filter to prevent division by zero errors
        grouped['Average_Cost'] = grouped.apply(
            lambda x: x['Total_Value'] / x['Quantity'] if x['Quantity'] > 0 else 0, axis=1
        )

        # Final cleanup: keep only the requested columns
        result = grouped[['Stock_Code', 'Description', 'Average_Cost']]

        # Save to a new Excel file
        result.to_excel(output_file, index=False)
        print(f"Success! Calculated data saved to '{output_file}'")

    except Exception as e:
        print(f"An error occurred: {e}")

# --- Configuration ---
input_filename = 'your_file_name.xlsx' # Change this to your actual file name
output_filename = 'Average_Cost_Report.xlsx'

# Run the function
calculate_average_cost(input_filename, output_filename)