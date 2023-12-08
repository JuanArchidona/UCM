package org.ntic.entregable

import scala.io.Source
import scala.util.{Try, Using}

object FileUtils {

  val delimiter: String = FlightsLoaderConfig.delimiter
  val headersLength: Int = FlightsLoaderConfig.headersLength
  val columnIndexMap: Map[String, Int] = FlightsLoaderConfig.columnIndexMap

  def isInvalid(line: String): Boolean = {
    line.isEmpty || line.split(delimiter, -1).filter(_.nonEmpty).length != headersLength
  }

  def loadFile(filePath: String): Seq[Flight] = {
    Using(Source.fromFile(filePath)) { source =>
      val linesList = source.getLines().toList
      val headers = linesList.head.split(delimiter, -1)
      require(headers.length == headersLength, "Número incorrecto de encabezados.")
      val rows = linesList.tail
      val (validRows, invalidRows) = rows.partition(line => !isInvalid(line))
      invalidRows.foreach(row => println(s"Fila inválida detectada: $row"))
      validRows.map { line =>
        val fields = line.split(delimiter, -1)
        Flight.fromString(fields, delimiter, columnIndexMap)
      }
    }.recover {
      case ex: Exception =>
        println(s"Error al leer el archivo: ${ex.getMessage}")
        Seq.empty[Flight]
    }.get
  }
}
