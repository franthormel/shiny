import pandas as pd
from shared import create_date

df = pd.read_csv('trade.csv')
df.exports = pd.to_numeric(df.exports).astype(float)
df.imports = pd.to_numeric(df.imports).astype(float)

df['balance_of_trade'] = df.apply(lambda row: row.exports - row.imports, axis=1)
df['total_trade'] = df.apply(lambda row: row.exports + row.imports, axis=1)

def calc_growth_rate(df, col):
    return df[col].pct_change().apply(lambda row: row * 100)

# NOTE: All data
df_all = df.copy().set_index('year').sum(numeric_only=True)

df['imports_growth_rate'] = calc_growth_rate(df, 'imports')
df['exports_growth_rate'] = calc_growth_rate(df, 'exports')
df['balance_of_trade_growth_rate'] = calc_growth_rate(df, 'balance_of_trade')
df['total_trade_growth_rate'] = calc_growth_rate(df, 'total_trade')
df['date'] = df.apply(lambda row: create_date(row), axis=1)

# NOTE: Yearly data
column_rates = ["imports_growth_rate", "exports_growth_rate", "balance_of_trade_growth_rate", "total_trade_growth_rate"]
column_rates_src = ["imports", "exports", "balance_of_trade", "total_trade"]

df_year = df.copy()
df_year.set_index('year')
df_year = df_year.groupby('year')
df_year = df_year.sum(numeric_only=True)

for i, column_rate in enumerate(column_rates):
    column_rate_src = column_rates_src[i]
    df_year[column_rate] = calc_growth_rate(df_year, column_rate_src)

# NOTE: Monthly data
# Group by month per year
df_month_each_year = df.pivot(index="year", columns="month")

def categorize_col_vals(df, col, type=''):
    # Get column values
    new_df = pd.DataFrame(df[col]).rename(columns={col: "values"})
    
    if type == '':
        type = col
    
    new_df['type'] = type
    new_df['date'] = df['date']
    return new_df

# NOTE: Charts (all)
df_all_chart_import_exports = pd.concat([
    categorize_col_vals(df, "exports", "Exports"),
    categorize_col_vals(df, "imports", "Imports")
])

df_all_chart_import_exports_growth_rate = pd.concat([
    categorize_col_vals(df, "exports_growth_rate", "Exports"),
    categorize_col_vals(df, "imports_growth_rate", "Imports")
])
