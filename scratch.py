import pickle
import pandas as pd

f = pickle.load(open("data/feature_text.pkl", "rb"))
print("feature_text type:", type(f))
if isinstance(f, str):
    print("feature_text is a string of length:", len(f))
elif isinstance(f, dict):
    print("feature_text is a dict with keys:", list(f.keys())[:5])
else:
    print("feature_text is something else")

df = pd.read_csv("data/data-viz1.csv")
print("Columns in data-viz1.csv:", df.columns.tolist())
if "features" in df.columns:
    print("First few features:")
    print(df[["sector", "features"]].head())

