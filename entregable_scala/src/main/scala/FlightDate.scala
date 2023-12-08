package org.ntic.entregable

import java.time.format.DateTimeFormatter
import java.time.LocalDate

case class FlightDate(day: Int, month: Int, year: Int) {
  require(year >= 1987, "El año debe ser 1987 o posterior")
  require(month >= 1 && month <= 12, "Mes inválido.")
  require(day >= 1 && day <= 31, "Día inválido.")

  lazy override val toString: String = f"$day%02d/$month%02d/${year % 100}%02d"
}

object FlightDate {
  def fromString(dateStr: String): FlightDate = {
    val datePart = dateStr.split(" ")(0)
    val parts = datePart.split("/")
    if (parts.length != 3) throw new IllegalArgumentException("Formato de fecha inválido.")

    val month = parts(0).toInt
    val day = parts(1).toInt
    val year = parts(2).toInt

    require(month >= 1 && month <= 12, "Mes inválido.")
    require(day >= 1 && day <= 31, "Día inválido.")
    require(year >= 1987, "Año inválido.")

    FlightDate(day, month, year)
  }
}




