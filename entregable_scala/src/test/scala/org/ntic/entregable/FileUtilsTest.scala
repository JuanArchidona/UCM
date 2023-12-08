package org.ntic.entregable

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class FileUtilsTest extends AnyFlatSpec with Matchers {
  "A line from a file" should "be invalid if it does not have the expected number of fields" in {
    val singleRowWithEmptyFields = """7/1/2023 12:00:00 AM;10257;ALB;Albany, NY;NY;11278;DCA;Washington, DC;VA;;;;"""
    FileUtils.isInvalid(singleRowWithEmptyFields) shouldBe true
  }

  "A line from a file" should "be valid if it has the expected number of fields" in {
    val singleRowWithAllFields = """7/1/2023 12:00:00 AM;10257;ALB;Albany, NY;NY;11057;CLT;Charlotte, NC;NC;1128;-9.00;1320;-25.00"""
    FileUtils.isInvalid(singleRowWithAllFields) shouldBe false
  }
}


