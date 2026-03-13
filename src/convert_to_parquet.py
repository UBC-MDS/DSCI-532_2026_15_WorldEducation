"""
Quick script to convert the processed CSV to Parquet format.
Run this once to generate the parquet file needed for lazy loading.
"""
import pandas as pd

# Read the existing processed CSV
df = pd.read_csv("../data/processed/processed_global_education.csv", encoding='latin-1', index_col=0)

# Save as Parquet
df.to_parquet("data/processed/processed_global_education.parquet", index=False)

print("  Successfully converted CSV to Parquet format!")
print(f"  Rows: {len(df)}")
print(f"  Columns: {len(df.columns)}")
print(f"  Output: data/processed/processed_global_education.parquet")
