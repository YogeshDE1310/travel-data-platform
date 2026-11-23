# Databricks notebook source
from pyspark.sql.functions import (
    col, to_date, count, sum as _sum, countDistinct, coalesce, lit
)

base = "abfss://travel-events@traveldatayogesh.dfs.core.windows.net"

silver_path = f"{base}/silver/travel_events/"
gold_daily_path    = f"{base}/gold/daily_event_summary/"
gold_customer_path = f"{base}/gold/customer_summary/"
gold_route_path    = f"{base}/gold/route_summary/"

# COMMAND ----------

silver_df = (
    spark.read.format("delta").load(silver_path)
    .withColumn("event_date", to_date(col("event_time")))
)

# Make sure amount columns exist and nulls become 0 for clean sums
for c in ["booking_amount", "amount", "refund_amount"]:
    if c not in silver_df.columns:
        silver_df = silver_df.withColumn(c, lit(0.0))
    silver_df = silver_df.withColumn(c, coalesce(col(c), lit(0.0)))

# COMMAND ----------

# Gold 1: daily summary by event type
daily_df = (
    silver_df.groupBy("event_date", "event_type")
    .agg(
        count("*").alias("event_count"),
        countDistinct("customer_id").alias("unique_customers"),
        _sum("booking_amount").alias("total_booking_amount"),
        _sum("amount").alias("total_amount"),
        _sum("refund_amount").alias("total_refund_amount"),
    )
)

(daily_df.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").save(gold_daily_path))

# COMMAND ----------

# Gold 2: per-customer summary
customer_df = (
    silver_df.groupBy("customer_id")
    .agg(
        count("*").alias("total_events"),
        _sum("booking_amount").alias("total_booking_amount"),
        _sum("refund_amount").alias("total_refund_amount"),
    )
)

(customer_df.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").save(gold_customer_path))

# COMMAND ----------

# Gold 3: route summary (source city -> destination city)
route_df = (
    silver_df
    .filter(col("source_city_id").isNotNull() & col("destination_city_id").isNotNull())
    .groupBy("source_city_id", "destination_city_id")
    .agg(
        count("*").alias("event_count"),
        _sum("booking_amount").alias("total_booking_amount"),
    )
)

(route_df.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").save(gold_route_path))

# COMMAND ----------

for name, p in [("daily", gold_daily_path), ("customer", gold_customer_path), ("route", gold_route_path)]:
    print(f"Gold {name} rows:", spark.read.format("delta").load(p).count())