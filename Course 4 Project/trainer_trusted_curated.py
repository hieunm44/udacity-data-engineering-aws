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

# Script generated for node Step Trainer Trusted
step_trainer_trusted_node174355678953 = glueContext.create_dynamic_frame.from_catalog(
    database="workspace",
    table_name="step_trainer_trusted",
    transformation_ctx="step_trainer_trusted_node174355678953",
)

# Script generated for node Accelerometer Trusted
accelerometer_trusted_node4 = glueContext.create_dynamic_frame.from_catalog(
    database="workspace",
    table_name="accelerometer_trusted",
    transformation_ctx="accelerometer_trusted_node4",
)

# Script generated for node Join Customer and Step Trainer
join_customerand_step_trainer_node174355679023 = Join.apply(
    frame1=accelerometer_trusted_node4,
    frame2=step_trainer_trusted_node174355678953,
    keys1=["timestamp"],
    keys2=["sensorreadingtime"],
    transformation_ctx="join_customerand_step_trainer_node174355679023",
)

# Script generated for node Drop Fields
drop_fields_node174355679764 = DropFields.apply(
    frame=join_customerand_step_trainer_node174355679023,
    paths=["user"],
    transformation_ctx="drop_fields_node174355679764",
)

# Script generated for node Step Trainer Trusted
step_trainer_trusted_node174355679493 = glueContext.write_dynamic_frame.from_catalog(
    frame=drop_fields_node174355679764,
    database="workspace",
    table_name="machine_learning_curated",
    transformation_ctx="step_trainer_trusted_node174355679493",
)

job.commit()
