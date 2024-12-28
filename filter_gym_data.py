"""
Nathan Scott
Personal Project
Sort through data for Hydra Labs
"""

import pandas as pd

# Load in file
filename = 'scraped_hydra_data.xlsx'
sheet_name = 'Original'
output_sheet_name = 'Cleaned Data'
df = pd.read_excel(filename, sheet_name=sheet_name)

# Show data size
print(f"Initial data size: {df.shape}")

# Create a copy of the data for filtering
filtered_df = df.copy()

# Remove duplicates
filtered_df.drop_duplicates(subset=['Link'], keep='first', inplace=True)


# Fill NaN with empty string temporarily to avoid errors
filtered_df['Title'] = filtered_df['Title'].fillna('').astype(str)

# Remove entries with unwanted keywords in Title
keywords_to_exclude = ['top 10', 'best of', 'review', 'comparison', 'guide', 'directory']
filtered_df = filtered_df[~filtered_df['Title'].str.lower().str.contains('|'.join(keywords_to_exclude))]

# Display cleaned data size
print(f"Cleaned data size: {filtered_df.shape}")

# Save filtered data to a new sheet
with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    filtered_df.to_excel(writer, sheet_name=output_sheet_name, index=False)

print(f"Filtered data written to '{output_sheet_name}' in {filename}")
