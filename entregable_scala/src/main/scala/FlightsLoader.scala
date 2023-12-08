package org.ntic.entregable

import java.io._

object FlightsLoader extends App {

  def writeObject(flights: Seq[Flight], outputFilePath: String): Unit = {
    val out = new ObjectOutputStream(new FileOutputStream(outputFilePath))
    try {
      out.writeObject(flights)
    } finally {
      out.close()
    }
  }

  val flights = FileUtils.loadFile(FlightsLoaderConfig.filePath)

  for (origin <- FlightsLoaderConfig.filteredOrigin) {

    val filteredFlights: Seq[Flight] = flights.filter(_.origin.code == origin)

    val delayedFlights: Seq[Flight] = filteredFlights.filter(_.isDelayed).sorted

    val notDelayedFlights: Seq[Flight] = filteredFlights.filterNot(_.isDelayed).sorted

    val flightObjPath: String = s"${FlightsLoaderConfig.outputDir}${File.separator}$origin.obj"

    val delayedFlightsObjPath: String = s"${FlightsLoaderConfig.outputDir}${File.separator}${origin}_delayed.obj"

    writeObject(notDelayedFlights, flightObjPath)

    writeObject(delayedFlights, delayedFlightsObjPath)
  }
}
