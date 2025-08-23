from google.cloud import bigquery
import pandas as pd
import numpy as np

client = bigquery.Client()


query = """
SELECT 
  TIMESTAMP_TRUNC(TIMESTAMP_MICROS(event_timestamp), MINUTE) AS minute,
  event_name,
  user_pseudo_id,
  traffic_source.medium AS traffic_medium,
  geo.country AS country,
  CASE WHEN ecommerce.transaction_id IS NOT NULL THEN 1 ELSE 0 END AS purchase_flag,
  ecommerce.purchase_revenue AS revenue
FROM 
  `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE 
  _TABLE_SUFFIX BETWEEN '20201101' AND '20210130'
  AND event_name IN ('session_start', 'view_item', 'add_to_cart', 'begin_checkout', 'purchase')
ORDER BY minute, user_pseudo_id
"""

df = client.query(query).to_dataframe()
print(df.head())
print(f"Total rows: {len(df)}")


df.shape


df["variant"] = np.where(
    np.mod(df["user_pseudo_id"].apply(lambda x: hash(x)), 2) == 0, "A", "B"
)


funnel_counts = (
    df.groupby(["variant", "event_name"])["user_pseudo_id"]
    .nunique()
    .reset_index(name="unique_users")
)

funnel_order = [
    "session_start",
    "view_item",
    "add_to_cart",
    "begin_checkout",
    "purchase",
]
funnel_counts["event_name"] = pd.Categorical(
    funnel_counts["event_name"], categories=funnel_order, ordered=True
)
funnel_counts = funnel_counts.sort_values(["variant", "event_name"])


funnel_rates = []
for variant in funnel_counts["variant"].unique():
    variant_data = funnel_counts[funnel_counts["variant"] == variant].sort_values(
        "event_name"
    )
    users_at_start = variant_data.iloc[0]["unique_users"]
    variant_data = variant_data.assign(
        conv_rate_total=lambda x: x["unique_users"] / users_at_start,
        conv_rate_step=lambda x: x["unique_users"] / x["unique_users"].shift(1),
    )
    funnel_rates.append(variant_data)

funnel_rates = pd.concat(funnel_rates)


revenue_stats = (
    df[df["purchase_flag"] == 1]
    .groupby("variant")
    .agg(total_revenue=("revenue", "sum"), total_buyers=("user_pseudo_id", "nunique"))
    .assign(avg_revenue_per_buyer=lambda x: x["total_revenue"] / x["total_buyers"])
    .reset_index()
)

# df.to_pickle("../AB Testing/raw/dataset_ecommerce.pkl")


df.to_csv("../AB Testing/raw/dataset_ecommerce.csv", index=False)
