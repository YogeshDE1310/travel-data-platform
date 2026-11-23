# Databricks notebook source
from pyspark.sql.functions import col, to_timestamp

base = "abfss://travel-events@traveldatayogesh.dfs.core.windows.net"

bronze_path = f"{base}/bronze/travel_events/"
silver_path = f"{base}/silver/travel_events/"

# COMMAND ----------

bronze_df = spark.read.format("delta").load(bronze_path)
print("Bronze count:", bronze_df.count())

# COMMAND ----------

# Cast only the columns that exist, so a missing column doesn't break the job
cast_map = {
    "customer_id": "long",
    "source_city_id": "long",
    "destination_city_id": "long",
    "airline_id": "long",
    "hotel_id": "long",
    "booking_amount": "double",
    "amount": "double",
    "refund_amount": "double",
}

silver_df = bronze_df
for c, t in cast_map.items():
    if c in silver_df.columns:
        silver_df = silver_df.withColumn(c, col(c).cast(t))

silver_df = silver_df.withColumn("event_time", to_timestamp(col("event_time")))

# COMMAND ----------

# Data quality: drop rows missing key fields, then remove duplicates
# (ignoring ingestion metadata so re-ingested copies count as duplicates)
meta_cols = [c for c in ["ingestion_time", "source_file", "_rescued_data"] if c in silver_df.columns]
dedupe_cols = [c for c in silver_df.columns if c not in meta_cols]

silver_df = (
    silver_df
    .filter(col("event_type").isNotNull())
    .filter(col("customer_id").isNotNull())
    .filter(col("event_time").isNotNull())
    .dropDuplicates(dedupe_cols)
)

# COMMAND ----------

(silver_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(silver_path))

silver_check = spark.read.format("delta").load(silver_path)
print("Silver count:", silver_check.count())
silver_check.show(5, truncate=False)