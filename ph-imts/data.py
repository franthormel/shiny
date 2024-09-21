# %%
import pandas as pd

# %%
# Read CSV and convert some columns to apprropriate data type
df = pd.read_csv('trade.csv')
df.exports = pd.to_numeric(df.exports).astype(float)
df.imports = pd.to_numeric(df.imports).astype(float)

# %%
df['botg'] = df.apply(lambda row: row.exports - row.imports, axis=1)
df['total_trade'] = df.apply(lambda row: row.exports + row.imports, axis=1)

# %%
df_all = df.copy().set_index('year').sum(numeric_only=True)

# %%
df['imports_growth_rate'] = df['imports'].pct_change()
df['exports_growth_rate'] = df['exports'].pct_change()
df['botg_growth_rate'] = df['botg'].pct_change()
df['total_trade_growth_rate'] = df['total_trade'].pct_change()

# %%
# Aggregate yearly
column_rates = ["imports_growth_rate", "exports_growth_rate", "botg_growth_rate", "total_trade_growth_rate"]
column_rates_src = ["imports", "exports", "botg", "total_trade"]

df_yearly = df.copy()
df_yearly.set_index('year')
df_yearly = df_yearly.groupby('year')
df_yearly = df_yearly.sum(numeric_only=True)

for i, column_rate in enumerate(column_rates):
    column_rate_src = column_rates_src[i]
    df_yearly[column_rate] = df_yearly[column_rate_src].pct_change()

# %%
df_month_year = df.pivot(index="month", columns="year")

# %%
# Compare values of the same year (eg: Exports of February and March in 1991)
df_exports_1991 = df_month_year["exports"][1991].copy()

# %%
# Compare values of different years (eg: Monthly imports of the years 1994 & 1995)
df_imports = df_month_year["imports"].copy()
df_imports_1994 = df_imports[1994].copy()
df_imports_1995 = df_imports[1995].copy()

# %%
