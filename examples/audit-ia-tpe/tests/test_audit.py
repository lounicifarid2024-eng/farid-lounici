import unittest

from audit import evaluate, render_report


def item(**overrides):
    base = {
        "name": "Demandes recurrentes",
        "weekly_volume": 40,
        "minutes_per_case": 5,
        "repetitive_pct": 75,
        "data_sensitivity": "faible",
        "decision_impact": "faible",
    }
    base.update(overrides)
    return base


class TestDiagnostic(unittest.TestCase):
    def test_pilote_risque_faible(self):
        result = evaluate(item())
        self.assertEqual(result["decision"], "CANDIDAT A UN PILOTE")
        self.assertAlmostEqual(result["baseline_hours_per_week"], 3.33)

    def test_donnees_sensibles_bloquent_le_pilote(self):
        result = evaluate(item(data_sensitivity="eleve"))
        self.assertEqual(result["decision"], "REVUE HUMAINE PREALABLE")

    def test_impact_decisionnel_eleve_prioritaire_sur_mesures_manquantes(self):
        result = evaluate(item(decision_impact="eleve", weekly_volume=None))
        self.assertEqual(result["decision"], "REVUE HUMAINE PREALABLE")

    def test_mesures_manquantes_non_inventees(self):
        result = evaluate(item(minutes_per_case=None))
        self.assertEqual(result["decision"], "DONNEES A COMPLETER")
        self.assertIsNone(result["baseline_hours_per_week"])

    def test_faible_repetition_alternative_non_ia(self):
        result = evaluate(item(repetitive_pct=25))
        self.assertEqual(result["decision"], "SIMPLIFIER D'ABORD")

    def test_sensibilite_moderee_avec_supervision(self):
        result = evaluate(item(data_sensitivity="modere"))
        self.assertEqual(result["decision"], "PILOTE SOUS CONDITIONS")

    def test_pourcentage_invalide_refuse(self):
        with self.assertRaises(ValueError):
            evaluate(item(repetitive_pct=125))

    def test_boolean_pas_un_nombre(self):
        with self.assertRaises(ValueError):
            evaluate(item(weekly_volume=True))

    def test_rapport_identifie_donnees_fictives(self):
        report = render_report({"company": "Entreprise fictive", "processes": [item()]})
        self.assertIn("DONNEES FICTIVES", report)
        self.assertIn("pas a une economie promise", report)


if __name__ == "__main__":
    unittest.main()
