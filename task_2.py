import pandas as pd
#reading the csv file
df_users = pd.read_csv('users.csv')
#converting (user ceation time) string to datetime
df_users["created_at"] = pd.to_datetime(df_users["created_at"])
#sorting users according to created date descending order
df_users_sorted = df_users.sort_values(by='created_at',ascending=False)
#keeping the last record of each user
df_users_updated = df_users_sorted.drop_duplicates(subset=['name', 'email'], keep='first')
#sorting users according to id
df_users_final = df_users_updated.sort_values(by='ID',ascending=True)
#saving the dataframe to csv
df_users_final.to_csv('unique_users.csv', index=False)