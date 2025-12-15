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

# Script generated for node Accelerometer Landing
accelerometer_landing_node174355677327 = glueContext.create_dynamic_frame.from_catalog(
    database="workspace",
    table_name="accelerometer_landing",
    transformation_ctx="accelerometer_landing_node174355677327",
)

# Script generated for node Customer Trusted Zone
customer_trusted_zone_node2 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://cd0030bucket/workspace/customers/trusted/"],
        "recurse": True,
    },
    transformation_ctx="customer_trusted_zone_node2",
)

# Script generated for node Join Customer
join_customer_node174355678923 = Join.apply(
    frame1=customer_trusted_zone_node2,
    frame2=accelerometer_landing_node174355677327,
    keys1=["email"],
    keys2=["user"],
    transformation_ctx="join_customer_node174355678923",
)

# Script generated for node Drop Fields
drop_fields_node174355679384 = DropFields.apply(
    frame=join_customer_node1743556789235,
    paths=[
        "serialnumber",
        "sharewithpublicasofdate",
        "birthday",
        "registrationdate",
        "sharewithresearchasofdate",
        "customername",
        "email",
        "lastupdatedate",
        "phone",
        "sharewithfriendsasofdate",
        "timestamp",
    ],
    transformation_ctx="drop_fields_node174355679384",
)

# Script generated for node AWS Glue Data Catalog
AWS_glue_data_catalog_node1809562500566 = glueContext.write_dynamic_frame.from_catalog(
    frame=drop_fields_node174355679384,
    database="workspace",
    table_name="accelerometer_trusted",
    transformation_ctx="AWS_glue_data_catalog_node1809562500566",
)

job.commit()
