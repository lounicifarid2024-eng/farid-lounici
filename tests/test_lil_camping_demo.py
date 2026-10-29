import unittest

from src.lil_camping_demo import answer_question, normalized


class CampingDemoTests(unittest.TestCase):
    def test_wifi(self):
        self.assertEqual(answer_question("Y a-t-il du WiFi ?")["category"], "wifi")

    def test_accented_reception(self):
        result = answer_question("Quels sont les horaires de la réception ?")
        self.assertEqual(result["status"], "FAQ")
        self.assertEqual(result["category"], "reception")

    def test_pool_requires_specific_time_question(self):
        self.assertEqual(answer_question("Je cherche la piscine")["status"], "HUMAN")
        self.assertEqual(answer_question("Quels horaires piscine ?")["category"], "piscine")

    def test_booking_escalates_before_wifi_keyword(self):
        result = answer_question("Je veux réserver et avoir le wifi.")
        self.assertEqual(result["status"], "HUMAN")
        self.assertEqual(result["category"], "sensitive")

    def test_payment_and_emergency_escalate(self):
        self.assertEqual(answer_question("Je veux payer ma réservation")["status"], "HUMAN")
        self.assertEqual(answer_question("Une urgence santé")["status"], "HUMAN")

    def test_unknown_escalates(self):
        self.assertEqual(answer_question("Est-ce que vous avez un restaurant ?")["status"], "HUMAN")

    def test_empty_and_long_inputs(self):
        self.assertEqual(answer_question("")["status"], "HUMAN")
        self.assertEqual(answer_question("x" * 401)["status"], "HUMAN")

    def test_not_a_data_capture_system(self):
        self.assertNotIn("john@example.com", str(answer_question("john@example.com")))

    def test_normalization_and_type_safety(self):
        self.assertEqual(normalized("  RÉCEPTION  "), "reception")
        with self.assertRaises(TypeError):
            normalized(None)


if __name__ == "__main__":
    unittest.main()
