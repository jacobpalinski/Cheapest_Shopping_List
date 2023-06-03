import pandas as pd
df = pd.read_csv(r'australian_suburbs.csv')
print(df['suburb'].value_counts())