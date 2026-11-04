
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/sram_fault_dataset.csv")

if not file_path.exists():
    print("Dataset not found!")
else:
    df = pd.read_csv(file_path)

    print("=" * 50)
    print("SRAM DATASET SUCCESSFULLY LOADED")
    print("=" * 50)

    print("Shape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDataset information:")
    df.info()

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDataset downloaded and verified!")
