
from datetime import date

import calendar
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

def create_date(row):
    year = int(row['year'])
    month = list(calendar.month_abbr).index(row['month'])
    day = 1
    date_created = date(year, month, day)
    return date_created.strftime("%Y-%m-%d")

def get_df_col_vals(df, col, col_rename="values"):
    # Get column values
    new_df = pd.DataFrame(df[col]).rename(columns={col: col_rename})
    new_df['type'] = col
    
    # Add date in YYYY-MM-DD format
    new_df['date'] = df.apply(lambda row: create_date(row), axis=1)
    
    return new_df

# Charts (all)
frames = [
    get_df_col_vals(df, "exports"),
    get_df_col_vals(df, "imports")
]
df_chart_all = pd.concat(frames)
