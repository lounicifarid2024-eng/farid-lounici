# Démonstrateur public — LIL Audit IA TPE

**Statut : démonstrateur pédagogique, non validé chez un client.**

Ce projet présente une étape simple du diagnostic métier conçu par Lounici Intelligence Lab : à partir de processus fictifs, il distingue une piste de pilote, une simplification sans IA, des données insuffisantes et les situations nécessitant une revue humaine.

Il utilise uniquement la bibliothèque standard de Python. **Aucun appel à une IA, aucun service externe et aucune promesse de ROI.** Ce code n'est pas le produit commercial complet.

## Exécution

Depuis ce dossier :

```bash
python3 audit.py --input entreprise_fictive.json --output rapport_demo.md
python3 -m unittest discover -s tests -v
```

Le rapport Markdown sera créé localement. Les calculs de charge représentent seulement le volume et le temps déclarés ; ils ne représentent pas du temps économisé.

## Champs du fichier d'exemple

| Champ | Description |
| --- | --- |
| `name` | Nom du processus, sans donnée personnelle |
| `weekly_volume` | Nombre de cas par semaine ou `null` |
| `minutes_per_case` | Minutes par cas ou `null` |
| `repetitive_pct` | Part répétitive de 0 à 100 ou `null` |
| `data_sensitivity` | `faible`, `modere` ou `eleve` |
| `decision_impact` | `faible`, `modere` ou `eleve` |

## Logique de décision

1. Impact décisionnel ou sensibilité élevés : **revue humaine préalable**, jamais d'automatisation recommandée automatiquement.
2. Mesures manquantes : **données à compléter**, sans chiffre inventé.
3. Risque modéré : **pilote sous conditions** après examen des droits, accès et contrôles.
4. Faible risque et au moins 60 % de répétitions : **candidat à un pilote**, à comparer aux alternatives sans IA.
5. Sinon : **simplifier d'abord**.

Ces règles sont illustratives : elles ne remplacent ni un audit professionnel, ni une analyse juridique/RGPD, ni une analyse de sécurité.

## Limites

- Les niveaux de risque sont déclarés dans le JSON et non vérifiés automatiquement.
- Le seuil de 60 % est une convention de démonstration, non une norme externe.
- Les informations sont fictives ; ne pas utiliser de vrais fichiers clients sans autorisation.
- Un professionnel doit valider toute recommandation, notamment pour les sujets sensibles.
- Le code ne constitue ni un système d'évaluation des salariés ni un outil de décision individuelle.

**Provenance :** Lounici Intelligence Lab, novembre 2026. Le démonstrateur librement consultable reste distinct du kit commercial payant. Aucune licence de réutilisation n'est accordée par le seul fait de rendre le dépôt public ; les conditions de licence sont à définir.
