package org.ntic.entregable

case class Time(hours: Int, minutes: Int) extends Ordered[Time] {
  require(hours >= 0 && hours < 24, "La hora debe estar entre 0 y 23.")
  require(minutes >= 0 && minutes < 60, "Los minutos deben estar entre 0 y 59.")

  val totalMinutes: Int = hours * 60 + minutes

  override def compare(that: Time): Int = this.totalMinutes - that.totalMinutes

  def addMinutes(m: Int): Time = {
    val total = totalMinutes + m
    val newHours = (total / 60) % 24
    val newMinutes = total % 60
    Time(newHours, newMinutes)
  }

  override def toString: String = f"$hours%02d:$minutes%02d"
}

object Time {
  def fromString(timeStr: String): Time = {
    val formatted = if (timeStr.length == 4) timeStr else f"${timeStr.toInt}%04d"
    val hours = formatted.substring(0, 2).toInt
    val minutes = formatted.substring(2).toInt
    Time(hours, minutes)
  }

  def fromMinutes(minutes: Int): Time = {
    val normalizedMinutes = minutes % (24 * 60)
    Time(normalizedMinutes / 60, normalizedMinutes % 60)
  }
}
