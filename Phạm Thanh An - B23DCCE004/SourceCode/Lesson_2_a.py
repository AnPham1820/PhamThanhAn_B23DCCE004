import pandas as pd
import numpy as np

def convert_age(age_str):
    try:
        years, days = map(int, age_str.split("-"))
        return years + days / 365
    except (ValueError, AttributeError):
        return None

df = pd.read_csv("results.csv")
df.replace("N/a", np.nan, inplace=True)
df["DAge"] = df["Age"]
df["Age"] = df["Age"].apply(convert_age)

non_stat_cols = ["Name", "Team", "Nation", "Position", "DAge"]
stat_cols = [col for col in df.columns if col not in non_stat_cols]

for col in stat_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

display_cols = ["Name", "Nation", "Team", "Position", "Age"]
output = []

col_widths = {
    "Name": 28,
    "Nation": 10,
    "Team": 20,
    "Position": 12,
}

def format_header(metric):
    return (
        f"{'Name':<{col_widths['Name']}} "
        f"{'Nation':<{col_widths['Nation']}} "
        f"{'Team':<{col_widths['Team']}} "
        f"{'Position':<{col_widths['Position']}} "
        f"{metric}"
    )

def format_separator(metric):
    return f"{'_'*98} "

def format_row(row, col):
    value = row.get("DAge", "") if col == "Age" else f"{row[col]:.2f}"
    return (
        f"{row['Name']:<{col_widths['Name']}} "
        f"{row['Nation']:<{col_widths['Nation']}} "
        f"{row['Team']:<{col_widths['Team']}} "
        f"{row['Position']:<{col_widths['Position']}} "
        f"{value}"
    )


for col in stat_cols:
    if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
        continue

    cols_to_use = display_cols + ([col] if col not in display_cols else [])
    if col == "Age" and "DAge" not in cols_to_use:
        cols_to_use.append("DAge")
    temp_df = df[cols_to_use].dropna(subset=[col])

    if temp_df.empty:
        continue

    try:
        top3 = temp_df.nlargest(3, col)
        bottom3 = temp_df.nsmallest(3, col)
    except Exception as e:
        print(f"Error {col}: {e}")
        continue

    pretty_col = col
    output.append(f"══════════════════════════════════ {pretty_col} ══════════════════════════════════")

    output.append("TOP 3: ")
    output.append(format_header(pretty_col))
    output.append(format_separator(pretty_col))
    for _, row in top3.iterrows():
        output.append(format_row(row, col))
    output.append('-'*98)

    output.append("BOTTOM 3: ")
    output.append(format_header(pretty_col))
    output.append(format_separator(pretty_col))
    for _, row in bottom3.iterrows():
        output.append(format_row(row, col))

    output.append("\n")

try:
    with open("top_3.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print("Top 3 and bottom 3 statistics saved to 'top_3.txt'")
except Exception as e:
    print(f"Error saving 'top_3.txt': {e}")

