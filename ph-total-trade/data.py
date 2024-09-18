import pandas as pd

df = pd.read_csv('trade.csv')
df.exports = pd.to_numeric(df.exports).astype(float)
df.imports = pd.to_numeric(df.imports).astype(float)

df['year_month'] = df.apply(lambda row: f'{row.month} {row.year}', axis=1)
df['balance_of_trade'] = df.apply(lambda row: row.exports - row.imports, axis=1)
df['total_trade'] = df.apply(lambda row: row.exports + row.imports, axis=1)
