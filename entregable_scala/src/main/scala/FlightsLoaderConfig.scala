package org.ntic.entregable

import com.typesafe.config.{Config, ConfigFactory}
import scala.collection.JavaConverters._

object FlightsLoaderConfig {
  val config: Config = ConfigFactory.load()
  val flightsLoaderConfig: Config = config.getConfig("flightsLoader")
  val filePath: String = flightsLoaderConfig.getString("filePath")
  val hasHeaders: Boolean = flightsLoaderConfig.getBoolean("hasHeaders")
  val headersLength: Int = if (hasHeaders) flightsLoaderConfig.getStringList("headers").size() else 0
  val delimiter: String = flightsLoaderConfig.getString("delimiter")
  val outputDir: String = flightsLoaderConfig.getString("outputDir")
  val headers: List[String] = if (hasHeaders) flightsLoaderConfig.getStringList("headers").asScala.toList else List()
  val columnIndexMap: Map[String, Int] = headers.zipWithIndex.toMap
  val filteredOrigin: List[String] = flightsLoaderConfig.getStringList("filteredOrigin").asScala.toList
}

