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

s3_source = 's3://your-bucket-name/wx_data/'
rds_jdbc_url = 'jdbc:postgresql://your-rds-endpoint:5432/yourdbname'
rds_dbtable = 'public.weather_data'
rds_user = 'yourusername'
rds_password = 'yourpassword'

datasource0 = glueContext.create_dynamic_frame.from_options(
    connection_type="s3", 
    connection_options={"paths": [s3_source]}, 
    format="csv",
    format_options={"withHeader": True, "separator": "\t"}
)

applymapping1 = ApplyMapping.apply(
    frame = datasource0, 
    mappings = [
        ("col0", "string", "station_id", "string"), 
        ("col1", "string", "date", "string"), 
        ("col2", "int", "max_temp", "int"), 
        ("col3", "int", "min_temp", "int"), 
        ("col4", "int", "precipitation", "int")
    ]
)

glueContext.write_dynamic_frame.from_options(
    frame = applymapping1, 
    connection_type = "jdbc", 
    connection_options = {
        "url": rds_jdbc_url, 
        "dbtable": rds_dbtable, 
        "user": rds_user, 
        "password": rds_password
    }
)

job.commit()
