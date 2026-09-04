import pandas as pd

# File locations
benign_file = "dataset/Monday-WorkingHours.pcap_ISCX.csv"
ddos_file = "dataset/Friday-WorkingHours-Afternoon-DDoS.pcap_ISCX.csv"
portscan_file = "dataset/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"

print("Loading datasets...")

# Load the datasets
benign = pd.read_csv(benign_file)
ddos = pd.read_csv(ddos_file)
portscan = pd.read_csv(portscan_file)

print("Datasets loaded!")

# Give each dataset a clear label
benign["Attack_Type"] = "BENIGN"
ddos["Attack_Type"] = "DDoS"
portscan["Attack_Type"] = "PortScan"

# Combine them
data = pd.concat(
    [benign, ddos, portscan],
    ignore_index=True
)

print("\nCombined dataset:")
print("Total rows:", len(data))

print("\nTraffic distribution:")
print(data["Attack_Type"].value_counts())

# Save combined dataset
data.to_csv("dataset/combined.csv", index=False)

print("\nCombined dataset saved successfully!")