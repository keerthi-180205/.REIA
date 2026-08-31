import pickle
import pandas as pd

with open('/home/keerthi-180205/Documents/ML_Project1/data/location_distance.pkl', 'rb') as f:
    df = pickle.load(f)

print("Dataframe shape:", df.shape)
print("Dataframe head:")
print(df.iloc[:5, :5])
print("\nMax value:", df.max().max())
print("Min value:", df.min().min())
