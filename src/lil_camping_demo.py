"""Démo locale et fictive de triage FAQ camping — sans LLM, sans réseau, sans données client.

Ce code n'est PAS une solution WhatsApp, un agent IA autonome, un service de
réservation ou une preuve de performance en production.
"""
from __future__ import annotations

import json
import sys
import unicodedata
from typing import Literal, TypedDict


class TriageResult(TypedDict):
    status: Literal["FAQ", "HUMAN"]
    category: str
    response: str
    source: str


def normalized(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("La question doit être une chaîne de caractères.")
    return " ".join(
        "".join(
            char for char in unicodedata.normalize("NFKD", value.casefold())
            if not unicodedata.combining(char)
        ).split()
    )


def answer_question(question: str) -> TriageResult:
    """Répond uniquement à quelques cas fictifs non sensibles, sinon escalade."""
    q = normalized(question)
    if not q or len(q) > 400:
        return {
            "status": "HUMAN",
            "category": "invalid",
            "response": "Votre demande doit être vérifiée par une personne.",
            "source": "règle de sécurité",
        }

    sensitive = (
        "reservation", "reserver", "annul", "paiement", "payer",
        "rembours", "carte bancaire", "sante", "urgence", "allerg",
        "handicap", "mot de passe", "adresse personnelle",
    )
    if any(word in q for word in sensitive):
        return {
            "status": "HUMAN",
            "category": "sensitive",
            "response": "Cette demande nécessite une prise en charge par l'accueil.",
            "source": "règle de validation humaine",
        }

    if "wifi" in q or "wi fi" in q:
        return {
            "status": "FAQ",
            "category": "wifi",
            "response": "Exemple fictif : les informations Wi-Fi sont disponibles à l'accueil.",
            "source": "jeu de données de démonstration",
        }

    if ("horaire" in q or "heure" in q) and ("accueil" in q or "reception" in q):
        return {
            "status": "FAQ",
            "category": "reception",
            "response": "Exemple fictif : la réception ouvre de 9 h à 18 h.",
            "source": "jeu de données de démonstration",
        }

    if "piscine" in q and ("horaire" in q or "heure" in q):
        return {
            "status": "FAQ",
            "category": "piscine",
            "response": "Exemple fictif : la piscine est ouverte de 10 h à 19 h.",
            "source": "jeu de données de démonstration",
        }

    return {
        "status": "HUMAN",
        "category": "unknown",
        "response": "Je ne dispose pas d'une réponse vérifiée : l'accueil doit vous répondre.",
        "source": "règle de reprise humaine",
    }


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]).strip()
    print(json.dumps(answer_question(question), ensure_ascii=False, indent=2))
