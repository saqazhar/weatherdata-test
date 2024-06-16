import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

rds_jdbc_url = 'jdbc:postgresql://your-rds-endpoint:5432/yourdbname'
rds_user = 'yourusername'
rds_password = 'yourpassword'

datasource0 = glueContext.create_dynamic_frame.from_options(
    connection_type="jdbc", 
    connection_options={
        "url": rds_jdbc_url, 
        "dbtable": "public.weather_data", 
        "user": rds_user, 
        "password": rds_password
    }
)

datasource0_df = datasource0.toDF()
datasource0_df.createOrReplaceTempView("weather_data")

stats_df = spark.sql("""
SELECT
    station_id,
    YEAR(TO_DATE(date, 'YYYYMMDD')) AS year,
    AVG(CASE WHEN max_temp != -9999 THEN max_temp / 10.0 ELSE NULL END) AS avg_max_temp,
    AVG(CASE WHEN min_temp != -9999 THEN min_temp / 10.0 ELSE NULL END) AS avg_min_temp,
    SUM(CASE WHEN precipitation != -9999 THEN precipitation / 10.0 ELSE 0 END) AS total_precipitation
FROM weather_data
GROUP BY station_id, year
""")

stats_dynamic_frame = DynamicFrame.fromDF(stats_df, glueContext, "stats_dynamic_frame")

glueContext.write_dynamic_frame.from_options(
    frame = stats_dynamic_frame, 
    connection_type = "jdbc", 
    connection_options = {
        "url": rds_jdbc_url, 
        "dbtable": "public.weather_stats", 
        "user": rds_user, 
        "password": rds_password
    }
)

job.commit()
