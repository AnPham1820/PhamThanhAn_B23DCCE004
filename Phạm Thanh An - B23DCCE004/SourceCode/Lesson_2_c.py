import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("results.csv")

# Chọn đại diện 3 chỉ số tấn công và 3 chỉ số phòng thủ
attack_stats  = ['Goals', 'Assists', 'Expected Goals (xG)']
defense_stats = ['Tackles', 'Interceptions', 'Blocks']
selected_stats = attack_stats + defense_stats

sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'

plt.figure(figsize=(14, 8))  
plt.suptitle('', fontsize=16, fontweight='bold', x=1.02, y=1.02)
for i, stat in enumerate(selected_stats, 1):
    plt.subplot(2, 3, i)
    sns.histplot(df[stat].dropna(), kde=True, bins=20, 
                color='skyblue', edgecolor='w', linewidth=0.5)
    plt.title(f'{stat}')
    plt.xlabel('')
plt.tight_layout(pad=2.5)  
plt.suptitle('All Players', fontsize=30, x=0.5, y=0.98)
plt.savefig('Histograms_all_players.png', bbox_inches='tight')
print(f"Saved to file: {'Histograms_all_players.png'}")
plt.show()

teams_order = [
    "Liverpool", "Arsenal", "Manchester City", "Nott'ham Forest",
    "Newcastle Utd", "Chelsea", "Aston Villa", "Bournemouth",
    "Fulham", "Brighton", "Brentford", "Crystal Palace",
    "Everton", "Manchester Utd", "Wolves", "Tottenham",
    "West Ham", "Ipswich Town", "Leicester City", "Southampton"
]

for team in teams_order:
    if team not in df['Team'].values:
        continue

    team_df = df[df['Team'] == team]
    
    plt.figure(figsize=(14, 8))  
    plt.suptitle(team, y=1.02, fontsize=14, fontweight='bold') 
    
    for i, stat in enumerate(selected_stats, 1):
        ax = plt.subplot(2, 3, i)
        sns.histplot(team_df[stat].dropna(), kde=True, bins=20,
                    color='skyblue', edgecolor='w', linewidth=0.5)
        plt.title(f'{stat}')
        plt.xlabel('')
        
    plt.tight_layout(pad=2.5)
    plt.suptitle(f'{team}', fontsize=30, x=0.5, y=0.96)
    filename = f'Histograms_{team.replace(" ", "_").replace("/", "-")}.png'
    plt.savefig(filename, bbox_inches='tight')
    print(f"Saved to file: {filename}")
    plt.show()