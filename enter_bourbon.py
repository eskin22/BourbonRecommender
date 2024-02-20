import pandas as pd

bourbons = pd.read_csv("src/data/master_bourbon_list.csv")

new_bourbon = {}

for i, col in enumerate(bourbons.columns):
    val = input(f"{col.upper()} : ")
    if i != 0:
        val = int(val)
    new_bourbon[col] = val
    
bourbons = pd.concat([bourbons, pd.DataFrame([new_bourbon])], ignore_index=True)
    
bourbons.to_csv("src/data/master_bourbon_list.csv", index=False)