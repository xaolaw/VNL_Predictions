import pandas as pd

def determine_winner(row):
    score_A, score_B = int(row['result'][0]), int(row['result'][2])
    if score_A > score_B:
        return row['Team A']
    else:
        return row['Team B']


results_21 = pd.read_csv("vnl_2021_results.csv")
results_21["year"] = 2021
results_22 = pd.read_csv("vnl_2022_results.csv")
results_22["year"] = 2022
results_23 = pd.read_csv("vnl_2023_results.csv")
results_23["year"] = 2023

results = [results_21, results_22,results_23]

for result in results:
    result[['day','month']] = result['date'].str.split(' ', expand=True)
    result['full_date'] = pd.to_datetime(result['day'] + ' ' + result['month'] + ' ' + result['year'].astype(str), format="mixed")
    result['Winner'] = result.apply(determine_winner, axis=1)
    result.drop(['date','result','hour','month','day','year'], axis=1, inplace=True)


data = pd.concat([results_21, results_22, results_23])
data = data.rename(columns={'Team A': 'TeamA','Team B': 'TeamB','full_date':'Match_Date',})
data = data.replace({'TeamA': {'United States': 'USA'}, 'TeamB': {'United States': 'USA'}})

player_data = pd.read_csv('df_mens_indv_21_23.csv')
player_data['Match_Date'] = pd.to_datetime(player_data['Match_Date'],format='%d/%m/%Y', errors='coerce')
merged_data = pd.merge(data, player_data, on=['TeamA', 'TeamB', 'Match_Date'], how='inner')

player_info_data = pd.read_csv('df_mens_rosters_21_23.csv')
player_info_data = player_info_data[['Player_ID', 'Player Name', 'Position', 'Nationality', 'Age','Height','Year']]
merged_data = pd.merge(player_info_data,merged_data,on=['Player_ID','Year'], how='inner')

merged_data['Winner'] = merged_data['Nationality'] == merged_data['Winner']

merged_data.to_csv('../vnl_dataset.csv', index=False)

