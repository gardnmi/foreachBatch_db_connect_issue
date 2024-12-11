import os
from pathlib import Path

from databricks.sdk import WorkspaceClient
from loguru import logger
from pyspark.sql import SparkSession

from my_project.my_module import what_does_the_fox_say

FILE_PATH = Path(__file__).resolve()


def get_spark(serverless: bool = False, profile: str = "DEFAULT"):
    """
    Returns a SparkSession or DatabricksSession object based on the environment.

    Parameters:
        serverless (bool, optional): Flag indicating whether to use serverless mode. Defaults to False.
        profile (str, optional): The profile to use for the session. Defaults to "DEFAULT".

    Returns:
        SparkSession or DatabricksSession: The Spark session object based on the environment.
    """
    if "DATABRICKS_RUNTIME_VERSION" in os.environ:
        logger.info(
            "Running in Databricks environment. Returning SparkSession.\n")
        return SparkSession.builder.getOrCreate()

    from databricks.connect import DatabricksSession

    if serverless:
        logger.info(
            "Running in local environment. Returning DatabricksSession in serverless mode.\n")
        return DatabricksSession.builder.serverless().profile(profile).getOrCreate()

    logger.info("Running in local environment. Returning DatabricksSession.\n")
    return DatabricksSession.builder.profile(profile).getOrCreate()


def get_dbutils(spark):  # noqa: F821
    # Initialize the Spark session in case it is not already initialized
    try:
        if "DATABRICKS_RUNTIME_VERSION" in os.environ:
            from pyspark.dbutils import DBUtils

            return DBUtils(spark)
        else:
            return WorkspaceClient().dbutils

    # If spark is not defined, then we are running in a local environment
    except NameError:
        return WorkspaceClient().dbutils


def what_does_the_cow_say(batch_df=None, batch_id=None):

    if batch_df is not None:
        print(f"Processing batch {batch_id}")
        print(f"Batch count: {batch_df.count()}")

    return "Moo Moo Moo"


if __name__ == "__main__":

    spark = get_spark()
    logger.info("Testing local function `what_does_the_cow_say`")
    logger.info("Running `what_does_the_cow_say` outside of stream")
    logger.info(what_does_the_cow_say())
    logger.success("`what_does_the_cow_say` function completed\n")
    
    logger.info("Running `what_does_the_cow_say` inside of stream")
    df = spark.readStream.table("samples.nyctaxi.trips").writeStream.foreachBatch(
        what_does_the_cow_say).trigger(availableNow=True).start()
    df.awaitTermination()
    logger.success("`what_does_the_cow_say` stream completed\n")

    print("------------------------\n")

    logger.info("Testing imported function `what_does_the_fox_say`")
    logger.info("Running `what_does_the_fox_say` outside of stream")
    logger.info(what_does_the_fox_say())
    logger.success("`what_does_the_fox_say` function completed\n")
   
    logger.info("Running `what_does_the_fox_say` inside of stream")
    df = spark.readStream.table("samples.nyctaxi.trips").writeStream.foreachBatch(
        what_does_the_fox_say).trigger(availableNow=True).start()
    
    df.awaitTermination()
    logger.success("`what_does_the_fox_say` stream completed")