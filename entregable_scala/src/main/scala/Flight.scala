package org.ntic.entregable

case class Flight(flDate: String,
                  origin: AirportInfo,
                  dest: AirportInfo,
                  scheduledDepTime: Time,
                  scheduledArrTime: Time,
                  depDelay: Double,
                  arrDelay: Double) extends Ordered[Flight] {

  lazy val flightDate: FlightDate = FlightDate.fromString(flDate)

  lazy val actualDepTime: Time = scheduledDepTime.addMinutes(depDelay.toInt)

  lazy val actualArrTime: Time = scheduledArrTime.addMinutes(arrDelay.toInt)

  val isDelayed: Boolean = depDelay > 0 || arrDelay > 0

  override def compare(that: Flight): Int = this.actualArrTime.compare(that.actualArrTime)
}

object Flight {
  def fromString(fields: Array[String], delimiter: String, columnIndexMap: Map[String, Int]): Flight = {
    def getColValue(colName: String): String = fields(columnIndexMap(colName))

    val oriAirport = AirportInfo(
      airportId = getColValue("ORIGIN_AIRPORT_ID").toLong,
      code = getColValue("ORIGIN"),
      cityName = getColValue("ORIGIN_CITY_NAME"),
      stateAbr = getColValue("ORIGIN_STATE_ABR")
    )

    val destAirport = AirportInfo(
      airportId = getColValue("DEST_AIRPORT_ID").toLong,
      code = getColValue("DEST"),
      cityName = getColValue("DEST_CITY_NAME"),
      stateAbr = getColValue("DEST_STATE_ABR")
    )

    Flight(
      flDate = getColValue("FL_DATE"),
      origin = oriAirport,
      dest = destAirport,
      scheduledDepTime = Time.fromString(getColValue("DEP_TIME")),
      scheduledArrTime = Time.fromString(getColValue("ARR_TIME")),
      depDelay = getColValue("DEP_DELAY").toDouble,
      arrDelay = getColValue("ARR_DELAY").toDouble
    )
  }
}
