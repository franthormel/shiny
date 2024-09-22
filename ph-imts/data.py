
import pandas as pd

df = pd.read_csv('trade.csv')
df.exports = pd.to_numeric(df.exports).astype(float)
df.imports = pd.to_numeric(df.imports).astype(float)

df['balance_of_trade'] = df.apply(lambda row: row.exports - row.imports, axis=1)
df['total_trade'] = df.apply(lambda row: row.exports + row.imports, axis=1)

# NOTE: All data
df_all = df.copy().set_index('year').sum(numeric_only=True)

df['imports_growth_rate'] = df['imports'].pct_change()
df['exports_growth_rate'] = df['exports'].pct_change()
df['balance_of_trade_growth_rate'] = df['balance_of_trade'].pct_change()
df['total_trade_growth_rate'] = df['total_trade'].pct_change()

# NOTE: Yearly data
column_rates = ["imports_growth_rate", "exports_growth_rate", "balance_of_trade_growth_rate", "total_trade_growth_rate"]
column_rates_src = ["imports", "exports", "balance_of_trade", "total_trade"]

df_year = df.copy()
df_year.set_index('year')
df_year = df_year.groupby('year')
df_year = df_year.sum(numeric_only=True)

for i, column_rate in enumerate(column_rates):
    column_rate_src = column_rates_src[i]
    df_year[column_rate] = df_year[column_rate_src].pct_change()

# NOTE: Monthly data
# Group by month per year
df_month_each_year = df.pivot(index="year", columns="month")
