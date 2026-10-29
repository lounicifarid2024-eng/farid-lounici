# Démonstrateur camping — preuve technique minimale
*29 octobre 2026 — statut : prototype local fictif.*

`src/lil_camping_demo.py` illustre un traitement **déterministe** de quelques demandes de clients d'un camping fictif. Ce n'est **pas un modèle d'intelligence artificielle**, ni une connexion WhatsApp, ni une téléphonie ni une prise de réservation réelle.

## Exécuter
Python 3.11+ ; pas de dépendances externes.

```bash
python -m src.lil_camping_demo "Quels sont les horaires de la réception ?"
python -m src.lil_camping_demo "Je veux réserver et payer"
python -m unittest discover -s tests -p "test_*.py" -v
```

## Comportement
- FAQ uniquement sur Wi-Fi et horaires fictifs de réception/piscine.
- Demandes inconnues, confidentielles, réservations, paiements et urgences : reprise humaine.
- Aucune donnée réelle et aucune journalisation de client.
- Les textes de réponses sont étiquetés **« Exemple fictif »**, non utilisables tels quels dans un établissement.

## Limites et prochaines étapes
- Aucune mesure de latence, disponibilité, sécurité de production ou robustesse LLM.
- Une véritable intégration exige un référentiel de données de l'établissement tenu à jour, une authentification, des droits, un canal de communication sécurisé, un mécanisme d'escalade opérationnel, des tests de charge et des coûts documentés.
- Les cas sensibles exigent validation humaine et protection des données ; ne jamais ingérer de données client dans un dépôt GitHub.

**Objet de cette démo :** démontrer une discipline de cadrage et de reprise humaine, pas vendre prématurément un service achevé.
