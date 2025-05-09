import pandas as pd
import numpy as np

def age_to_decimal(age_str):
    try:
        years, days = map(int, age_str.split("-"))
        return years + days / 365.0
    except:
        return np.nan

df = pd.read_csv("results.csv")

non_stat = ["Name", "Nation", "Team", "Position"]
stat_cols = [c for c in df.columns if c not in non_stat]

df["Age"] = df["Age"].apply(age_to_decimal)

df[stat_cols] = df[stat_cols].apply(pd.to_numeric, errors="coerce")

funcs = ['median', 'mean', 'std']

global_metrics = {
    f"{func.capitalize()} of {col}": df[col].agg(func)
    for col in stat_cols
    for func in funcs
}
global_df = pd.DataFrame(global_metrics, index=['All'])

team_df = df.groupby("Team")[stat_cols].agg(funcs)
team_df.columns = [f"{func.capitalize()} of {col}" for col, func in team_df.columns]

result = pd.concat([global_df, team_df], axis=0)

result = result.reset_index() 
result.rename(columns={"index": "Team"}, inplace=True)

result.to_csv("results2.csv", index=True, encoding='utf-8-sig')

print("Saved results2.csv")