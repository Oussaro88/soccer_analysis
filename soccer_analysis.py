'''
# PROJECT GOALS
    Make a quick analysis about Italy performance in EURO 2020

# DQUESTIONS
    "How many goals have the team scored in average per game?",
    "How many minutes did the team played during the competition?",
    "Are there any correlations between the minutes played per game and the goal scored?"

'''


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV data
data = pd.read_csv('match_info.csv')


# Clean data (remove missing values)
data.dropna(inplace=True)

# Removing duplicates
data.drop_duplicates(inplace=True)

# Converting float columns to integers
data['ScoreAway'] = data['ScoreAway'].astype(int)
data['ScoreHome'] = data['ScoreHome'].astype(int)

print(data.head())

# Connect to the database
conn = sqlite3.connect('matchs.db')

# Create a table
data.to_sql('matchs', conn, index=False, if_exists='replace')

# Selecting all games Italy played
print("Games Italy played")
query = "SELECT * FROM matchs \
            WHERE hometeamname = 'Italy' OR awayteamname = 'Italy'"
result = conn.execute(query).fetchall()
for row in result:
    print(row)
print("\n")

# Get column names from cursor description
col_names = [desc[0] for desc in conn.execute(query).description]
df = pd.DataFrame(result, columns=col_names)
print(df.info())
print("\n")


# Total goles Italy scored
print("Goals Italy scored")
print("Home goals")
query = "SELECT ScoreHome \
            FROM matchs \
            WHERE hometeamname = 'Italy'"
result_home = conn.execute(query).fetchall()
for row in result_home:
    print(row)

print("Away goals")
query = "SELECT ScoreAway \
            FROM matchs \
            WHERE Awayteamname = 'Italy'"
result_away = conn.execute(query).fetchall()
for row in result_away:
    print(row)

print("Total goals")
query = "SELECT MATCHID, SCOREAWAY, SCOREHOME, (SCOREAWAY+SCOREHOME) AS TOTALGOALS\
            FROM matchs \
            WHERE Awayteamname = 'Italy' OR Hometeamname = 'Italy' \
            GROUP BY MATCHID"
result_sum = conn.execute(query).fetchall()
for row in result_sum:
    print(row)

col = ['MATCHID', 'SCOREAWAY', 'SCOREHOME', 'TOTALGOALS']
result_df_sum = pd.DataFrame(result_sum, columns=col)
print(result_df_sum.head())

print('\n')
print("Average goal")
query = "SELECT AVG(ScoreAway + ScoreHome) AS GOAL_AVG \
            FROM matchs \
            WHERE Awayteamname = 'Italy' OR Hometeamname = 'Italy'"
result_avg = conn.execute(query).fetchall()
for row in result_avg:
    print(row)

# Filtering the search and creating a DataFrame from the result
query = "SELECT HomeTeamName, AwayTeamName, ScoreHome, ScoreAway \
            FROM matchs \
            WHERE HomeTeamName = 'Italy' OR AwayTeamName = 'Italy'"
result_it = conn.execute(query).fetchall()
col = ['HomeTeamName', 'AwayTeamName', 'ScoreHome', 'ScoreAway']
result_df = pd.DataFrame(result_it, columns=col)
# Adding a column for the total goals
result_df['Total goals'] = result_df['ScoreHome'] + result_df['ScoreAway']
print(result_df)
print("\n")
print(result_df.describe().round(2))


# Fetching the number of minutes played by Italy during the competition
print("Total minutes played")
query = "Select HomeTeamName, AwayTeamName, MatchMinute, MATCHID \
            FROM matchs \
            WHERE Awayteamname = 'Italy' OR Hometeamname = 'Italy' \
                GROUP BY MATCHID"
result_minutes = conn.execute(query).fetchall()
col = ['HomeTeamName', 'AwayTeamName', 'MatchMinute', 'MATCHID']
result_df_min = pd.DataFrame(result_minutes, columns=col)
print(result_df_min)
print("\n")
print(result_df_min.describe().round(2))
print("\n")

'''
    Creating a bar plot for minutes played per game
'''
plt.bar(result_df_min.index,
        result_df_min['MatchMinute'], color='green')
plt.xlabel('Match ID')
plt.ylabel('Match minutes')
plt.title('Total Minutes played for each game')
plt.show()

print("Total minutes played")
query = "Select HomeTeamName, AwayTeamName, MAX(MatchMinute) \
            FROM matchs \
            WHERE Awayteamname = 'Italy' OR Hometeamname = 'Italy'"
result_most_min_played = conn.execute(query).fetchall()
print(result_most_min_played)


print("Total goal scored by minutes")
query = "Select HomeTeamName, AwayTeamName, MatchMinute, MATCHID, ScoreAway, ScoreHome \
            FROM matchs \
            WHERE Awayteamname = 'Italy' OR Hometeamname = 'Italy'"
result_goal_min = conn.execute(query).fetchall()
col = ['HomeTeamName', 'AwayTeamName', 'MatchMinute',
       'MATCHID', 'ScoreHome', 'ScoreAway']
result_df_goal_min = pd.DataFrame(result_goal_min, columns=col)
result_df_goal_min['TOTALGOALS'] = result_df_goal_min['ScoreHome'] + \
    result_df_goal_min['ScoreAway']
print(result_df_goal_min)
print("\n")
print(result_df_goal_min.describe().round(2))
print("\n")

'''
    Creating a bar plot for goals per minutes
'''
plt.bar(result_df_goal_min['TOTALGOALS'],
        result_df_goal_min['MatchMinute'], color='red', align='center')
plt.xlabel('Total Goals')
plt.ylabel('Minutes played')
plt.title('Total Goals for minutes played')
plt.show()


# Calculating the correlation between total goals scored and minutes played per game
print('Correlation between total goals scored and minutes played per game')
correaltion = result_df_goal_min['TOTALGOALS'].corr(
    result_df_goal_min['MatchMinute'])
print(correaltion)
print("There is acorrelation, but it's not very strong, therefore we can say that the minutes played per game \
      don't have a strong influence about the number of goals scored \
      WE can conclude that there is no causation effect")
