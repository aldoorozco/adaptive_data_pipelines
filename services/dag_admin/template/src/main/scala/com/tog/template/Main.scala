package com.tog.template

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import za.co.absa.spline.core.SparkLineageInitializer._
import java.time.LocalDate
import org.apache.log4j.{Logger, Level}

object Main {

  private def getSession: SparkSession = {
    val sparkSession = SparkSession.builder
      .appName("Adaptive data pipeline task")
      .config("hive.metastore.client.factory.class", "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory")
      .enableHiveSupport()
      .getOrCreate()
    sparkSession
  }

  private def getAllConf: String = {
    getSession.conf.getAll.map { case(k,v) => "Key: [%s] Value: [%s]" format (k,v)} mkString("","\n","\n")
  }

  def main(args: Array[String]) {
    val logger = Logger.getLogger(getClass.getName)
    logger.setLevel(Level.INFO)
    logger.info("Spark pipeline task")

    val sparkSession = getSession
    import sparkSession.implicits._

    sparkSession.sparkContext.setLogLevel("WARN")
    sparkSession.enableLineageTracking()

    logger.info(s"Configs $getAllConf")
    logger.info(s"Args $args")

    val sqlQuery = args(0)
    val destTable = args(1)
    val destPath = args(2)

    logger.info(s"SQL query:\n$sqlQuery")
    logger.info(s"Dumping results in $destTable")
    val result = sparkSession.sql(sqlQuery)
                    .withColumn("dateid", lit(LocalDate.now.toString))

    if (!destTable.trim.isEmpty) {
        result.write.mode("overwrite")
            .partitionBy("dateid")
            .option("path", destPath + "/results")
            .saveAsTable(destTable)
    } else {
        logger.error("Empty destination table!")
    }

    logger.info("Finished task")
  }
}
