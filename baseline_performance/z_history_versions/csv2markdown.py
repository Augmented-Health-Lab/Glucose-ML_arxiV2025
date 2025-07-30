import pandas as pd
import os

folders = ["zero_order_hold", "linear_regression"]

output_folder = "markdown_tables/"
os.makedirs(output_folder, exist_ok=True)

for folder in folders:
    for file in os.listdir(folder):
        print(f"Processing {folder}/{file}...")
        # Load your CSV file
        df = pd.read_csv(os.path.join(folder, file))

        # Extract numeric prefix and sort by it
        df['dataset_number'] = df['dataset'].str.extract(r'^(\d+)_').astype(float)
        df['dataset'] = df['dataset'].str.split('_').str[1]  # Remove the numeric prefix from 'dataset'
        df_sorted = df.sort_values(by='dataset_number').drop(columns='dataset_number')
        df.drop(columns='dataset_number', inplace=True)
        
        # Convert to Markdown
        markdown_table = df_sorted.to_markdown(index=False)

        # Print or save the Markdown
        # print(markdown_table)

        output_file = os.path.join(output_folder, f"{folder + '_' + file.replace('.csv', '.md')}")
        with open(output_file, "w") as f:
            f.write(markdown_table)