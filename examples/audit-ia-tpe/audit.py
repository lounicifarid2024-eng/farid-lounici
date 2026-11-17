#!/usr/bin/env python3
"""Demonstration locale de diagnostic de processus (sans IA, sans API)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

LEVELS = {"faible", "modere", "eleve"}


def nonnegative_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def evaluate(process):
    """Classer un processus selon des règles explicites, sans prédire un ROI."""
    if not isinstance(process, dict):
        raise ValueError("Chaque processus doit etre un objet JSON.")
    name = process.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Chaque processus doit avoir un nom non vide.")
    privacy = process.get("data_sensitivity")
    impact = process.get("decision_impact")
    if privacy not in LEVELS or impact not in LEVELS:
        raise ValueError(f"{name}: data_sensitivity et decision_impact doivent etre faible/modere/eleve.")

    volume = process.get("weekly_volume")
    minutes = process.get("minutes_per_case")
    repetitive = process.get("repetitive_pct")
    for field, value in [("weekly_volume", volume), ("minutes_per_case", minutes)]:
        if value is not None and not nonnegative_number(value):
            raise ValueError(f"{name}: {field} doit etre un nombre >= 0 ou null.")
    if repetitive is not None and (not nonnegative_number(repetitive) or repetitive > 100):
        raise ValueError(f"{name}: repetitive_pct doit etre entre 0 et 100 ou null.")

    baseline_hours = None if volume is None or minutes is None else round(volume * minutes / 60, 2)
    missing = [field for field, value in [
        ("weekly_volume", volume), ("minutes_per_case", minutes), ("repetitive_pct", repetitive)
    ] if value is None]

    if privacy == "eleve" or impact == "eleve":
        decision = "REVUE HUMAINE PREALABLE"
        reason = "Sensibilite des donnees ou impact decisionnel eleve : aucune automatisation sans analyse specialisee."
    elif missing:
        decision = "DONNEES A COMPLETER"
        reason = "Mesures insuffisantes pour prioriser ce processus."
    elif privacy == "modere" or impact == "modere":
        decision = "PILOTE SOUS CONDITIONS"
        reason = "Examiner les bases legales, l'acces aux donnees et les controles humains avant tout pilote."
    elif repetitive >= 60:
        decision = "CANDIDAT A UN PILOTE"
        reason = "Taches repetitives et risques declares faibles ; comparer avec des solutions sans IA."
    else:
        decision = "SIMPLIFIER D'ABORD"
        reason = "Standardiser le processus et mesurer les effets avant de tester l'IA."

    return {
        "name": name.strip(),
        "decision": decision,
        "reason": reason,
        "baseline_hours_per_week": baseline_hours,
        "missing_fields": missing,
        "non_ai_alternative": "FAQ, modele de reponse, formulaire structure ou regles de tri."
    }


def render_report(data):
    """Produire un brouillon Markdown ; validation par un professionnel requise."""
    if not isinstance(data, dict) or not isinstance(data.get("company"), str):
        raise ValueError("Le document doit contenir un champ company texte.")
    processes = data.get("processes")
    if not isinstance(processes, list) or not processes:
        raise ValueError("Le document doit contenir une liste non vide de processus.")
    results = [evaluate(item) for item in processes]
    lines = [
        "# Rapport de demonstration — Audit IA TPE",
        "",
        "**DONNEES FICTIVES — NE CONSTITUE PAS UN AUDIT CLIENT**",
        "",
        f"Organisation fictive : {data['company']}",
        "",
        "Ce calcul est deterministe et ne contacte aucun service externe.",
        "Le temps calcule correspond au volume de travail declare, pas a une economie promise.",
        "",
    ]
    for index, result in enumerate(results, 1):
        baseline = (f"{result['baseline_hours_per_week']:.2f} h/semaine"
                    if result["baseline_hours_per_week"] is not None else "non calculable")
        lines += [
            f"## {index}. {result['name']}",
            "",
            f"- Orientation : **{result['decision']}**",
            f"- Motif : {result['reason']}",
            f"- Charge actuelle declaree : {baseline}",
            f"- Champs manquants : {', '.join(result['missing_fields']) if result['missing_fields'] else 'aucun'}",
            f"- Solution sans IA a comparer : {result['non_ai_alternative']}",
            "",
        ]
    lines += [
        "## Conditions de validation",
        "",
        "- Verifier les donnees saisies avec l'entreprise.",
        "- Examiner les contraintes RGPD, securite et droits d'acces si des donnees reelles sont utilisees.",
        "- Faire approuver les recommandations par une personne competente.",
        "- Mesurer les resultats d'un pilote avant toute promesse de gain.",
        "",
        "_Lounici Intelligence Lab — demonstrateur public distinct du produit payant._",
    ]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Demonstration locale du diagnostic IA TPE")
    parser.add_argument("--input", required=True, type=Path, help="Fichier JSON synthetique")
    parser.add_argument("--output", required=True, type=Path, help="Destination du rapport Markdown")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    report = render_report(data)
    args.output.write_text(report, encoding="utf-8")
    print(f"Rapport cree : {args.output}")


if __name__ == "__main__":
    main()
