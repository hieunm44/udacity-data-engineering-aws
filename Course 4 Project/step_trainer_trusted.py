import sys
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

# Script generated for node Customer Curated
customer_curated_node174355672567 = glueContext.create_dynamic_frame.from_catalog(
    database="workspace",
    table_name="customer_curated",
    transformation_ctx="customer_curated_node174355672567",
)

# Script generated for node Step Trainer Landing
step_trainer_landing_node3 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://cd0030bucket/workspace/step_trainer/landing/"],
        "recurse": True,
    },
    transformation_ctx="step_trainer_landing_node3",
)

# Script generated for node Join Customer and Step Trainer
join_customer_and_step_trainer_node174355673940 = Join.apply(
    frame1=step_trainer_landing_node3,
    frame2=customer_curated_node174355672567,
    keys1=["serialNumber"],
    keys2=["serialnumber"],
    transformation_ctx="join_customer_and_step_trainer_node174355673940",
)

# Script generated for node Drop Fields
drop_fields_node174355675760 = DropFields.apply(
    frame=join_customer_and_step_trainer_node174355673940,
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
    ],
    transformation_ctx="drop_fields_node174355675760",
)

# Script generated for node Step Trainer Trusted
step_trainer_trusted_node174355672974 = glueContext.write_dynamic_frame.from_catalog(
    frame=drop_fields_node174355675760,
    database="workspace",
    table_name="step_trainer_trusted",
    transformation_ctx="step_trainer_trusted_node174355672974",
)

job.commit()