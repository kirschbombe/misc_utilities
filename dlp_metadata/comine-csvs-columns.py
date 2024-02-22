import pandas as pd

# 1. defines column name and files to merge
column = input("Enter column name:")
file1 = input("Path to file 1:")
file2 = input("Path to file 2:")

# Load the CSV files into dataframes
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Merge the dataframes using the "filename" column as a key
merged_df = pd.merge(df1, df2, on=column, how="outer")

# Write the merged dataframe to a new CSV file
merged_df.to_csv("merged.csv", index=False)