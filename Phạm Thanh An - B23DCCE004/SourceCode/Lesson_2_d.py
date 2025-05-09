import pandas as pd

df = pd.read_csv('results2.csv')

Team_mean = []

df['Total Mean Score'] = 0

for column_name in df.columns:
    if column_name.startswith('Mean of'): 
        team_with_highest_mean = df.loc[df[column_name].idxmax(), 'Team']
        
        highest_mean_value = df[column_name].max()
        
        Team_mean.append({
            'Attribute': column_name.replace('Mean of ', ''), 
            'Top Team': team_with_highest_mean,  
            'Mean Value': highest_mean_value  
        })
        
        print(f"The team with the highest '{column_name.replace('Mean of ', '')}' is '{team_with_highest_mean}', with Mean Value: {highest_mean_value}.")

        df['Total Mean Score'] += df[column_name].fillna(0) 

team_with_best_total_performance = df.loc[df['Total Mean Score'].idxmax(), 'Team']
highest_total_mean_score = df['Total Mean Score'].max()

print(f"\n🏆 The team with the best performance in the 2024-2025 Premier League season is '{team_with_best_total_performance}', with an average total score of {highest_total_mean_score}.")

df_team = pd.DataFrame(Team_mean)

output_file = 'Top_Teams.csv'

df_team.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n📁 The results have been saved to the file: {output_file}")