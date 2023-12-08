package org.ntic.entregable

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class FlightDateTest extends AnyFlatSpec with Matchers {
  "A FlightDate" should "be correctly initialized from string with a timestamp" in {
    val dateStr = "07/01/2023 12:00:00 AM"
    val expected = FlightDate(day = 1, month = 7, year = 2023)
    val result = FlightDate.fromString(dateStr.split(" ")(0)) // Usar solo la parte de la fecha
    result shouldEqual expected
  }

  it should "throw an IllegalArgumentException for incorrect string format" in {
    val dateStr = "7/1/2023/3 12:00:00 AM"
    assertThrows[IllegalArgumentException] {
      FlightDate.fromString(dateStr.split(" ")(0)) // Usar solo la parte de la fecha
    }
  }

  it should "be correctly initialized from date string without timestamp" in {
    val dateStr = "07/01/2023"
    val expected = FlightDate(day = 1, month = 7, year = 2023)
    val result = FlightDate.fromString(dateStr)
    result shouldEqual expected
  }
}



