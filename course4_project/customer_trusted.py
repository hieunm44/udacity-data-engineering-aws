import sys
import re
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 bucket
S3_bucket_node1676574227044 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://cd0030bucket/workspace/customers/landing/"],
        "recurse": True,
    },
    transformation_ctx="S3_bucket_node1676574227044",
)

# Script generated for node ApplyMapping
apply_mapping_node1 = Filter.apply(
    frame=S3_bucket_node1676574227044,
    f=lambda row: (not (row["sharewithresearchasofdate"] == 0)),
    transformation_ctx="apply_mapping_node1",
)

# Script generated for node AWS Glue Data Catalog
AWS_glue_data_catalog_node1743556770566 = glueContext.write_dynamic_frame.from_catalog(
    frame=apply_mapping_node1,
    database="workspace",
    table_name="customer_trusted",
    transformation_ctx="AWS_glue_data_catalog_node1743556770566",
)

job.commit()