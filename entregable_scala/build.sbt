ThisBuild / version := "0.1.0-SNAPSHOT"
ThisBuild / scalaVersion := "2.13.12"

val mainClassPath = "org.ntic.entregable.FlightsLoader"

lazy val root = (project in file("."))
  .settings(
    name := "entregable_scala",
    Compile / run / mainClass := Some(mainClassPath),
    Compile / packageBin / mainClass := Some(mainClassPath),
    assembly / mainClass := Some(mainClassPath),
    assembly / assemblyJarName := "flights_loader.jar",

    libraryDependencies ++= Seq(
      "com.typesafe" % "config" % "1.4.2",
      "org.scalatest" %% "scalatest" % "3.2.17" % Test
    )
  )

