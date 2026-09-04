import pandas as pd

file = "dataset/Monday-WorkingHours.pcap_ISCX.csv"

df = pd.read_csv(file, nrows=1000)

print("Dataset loaded successfully!")
print("\nRows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nColumn names:")
for column in df.columns:
    print(column)

print("\nFirst 5 rows:")
print(df.head())

print("\nLabels:")
print(df[" Label"].value_counts())