# NBA Next Season Points ML

Projet de Machine Learning visant à prédire le nombre de points par match d'un joueur NBA lors de la saison suivante.

## Objectif

L'objectif est de prédire `pts_next_season`, correspondant aux points par match d'un joueur lors de la saison N+1, à partir des informations disponibles jusqu'à la fin de la saison N.

Le projet cherche notamment à déterminer dans quelle mesure la production actuelle, le rôle offensif, l'âge, l'expérience, le contexte collectif et le poste permettent d'anticiper la production offensive future.

## Données

Les données proviennent principalement de la NBA API et couvrent les saisons 1996-97 à 2022-23.

Les sources utilisées comprennent :

- informations biographiques des joueurs ;
- statistiques individuelles de base ;
- statistiques individuelles avancées ;
- statistiques collectives ;
- rosters NBA.

Le dataset supervisé final contient :

- 9 911 joueur-saisons ;
- 251 colonnes ;
- une cible : `pts_next_season`.

Une observation correspond à un joueur pour une saison donnée.

## Workflow

Le projet suit les différentes phases du workflow ML :

1. Introduction et cadrage
2. Extraction multi-sources
3. EDA diagnostique
4. Nettoyage des données
5. Transformation et feature engineering
6. EDA analytique
7. Visualisation et storytelling
8. Modélisation Machine Learning
9. Chargement et documentation
10. Présentation et soutenance

## Feature Engineering

Plusieurs variables ont été créées afin d'enrichir les données disponibles :

- statistiques de la saison précédente ;
- variations par rapport à la saison précédente ;
- moyennes historiques calculées uniquement sur le passé ;
- points et tirs par minute ;
- taux de tirs à trois points ;
- taux de lancers francs ;
- ratio passes / pertes de balle ;
- groupes d'âge ;
- groupes d'expérience ;
- indicateurs rookie ;
- indicateurs multi-équipe ;
- disponibilité des informations de roster.

La cible `pts_next_season` est créée uniquement lorsqu'une saison N+1 consécutive est disponible.

## EDA analytique

Les analyses ont notamment montré que :

- environ 49,5 % des joueur-saisons évoluent d'au moins 2 points par match entre N et N+1 ;
- les jeunes joueurs progressent davantage en moyenne ;
- la progression offensive tend à devenir négative autour du milieu de la vingtaine ;
- le volume de tirs, le temps de jeu et l'usage offensif sont fortement associés au scoring futur ;
- `FGA` présente une corrélation d'environ 0,838 avec les points en N+1 ;
- les variables collectives de l'équipe ont une association directe beaucoup plus faible ;
- le poste décrit fortement le profil statistique d'un joueur, mais explique peu son évolution future.

## Modélisation

Le problème est traité comme une régression.

### Métrique principale

La métrique principale est la MAE, car elle permet d'exprimer directement l'erreur moyenne en points par match.

Les métriques complémentaires sont :

- RMSE ;
- R².

### Découpage temporel

Afin d'éviter qu'une saison future soit utilisée pour prédire artificiellement une saison passée, le dataset est séparé chronologiquement :

- Train : 1996-97 à 2011-12
- Validation : 2012-13 à 2016-17
- Test : 2017-18 à 2021-22

La validation croisée respecte également l'ordre temporel avec cinq folds.

### Baselines

Deux baselines ont été utilisées :

- `DummyRegressor(strategy="mean")`
- persistance : `PTS N+1 = PTS N`

La baseline de persistance constitue la référence principale à battre.

### Modèles comparés

Trois familles de modèles ont été comparées avec `GridSearchCV` :

- Ridge
- Decision Tree Regressor
- Random Forest Regressor

Le modèle retenu est :

    Ridge(alpha=100)

Le Ridge a été préféré au Random Forest car leurs performances étaient quasiment identiques sur la validation, tandis que le Ridge présentait moins de surapprentissage et une meilleure simplicité d'interprétation.

## Résultats finaux

Les performances sur le jeu de test 2017-18 à 2021-22 sont :

| Métrique | Ridge | Baseline persistance |
|---|---:|---:|
| MAE | 2.393 | 2.558 |
| RMSE | 3.104 | 3.354 |
| R² | 0.775 | 0.737 |

Le Ridge réduit la MAE d'environ 6,5 % par rapport à la baseline de persistance.

## Structure du projet

    data/
    ├── raw/
    ├── cleaned/
    ├── processed/
    └── curated/

    docs/
    ├── data_dictionary.csv
    └── transformations.md

    exports/
    └── nba_next_season_dataset_v1_YYYYMMDD.csv

    models/
    ├── nba_pts_ridge_pipeline_v1_YYYYMMDD.joblib
    └── nba_pts_model_metadata_v1_YYYYMMDD.json

    reports/
    ├── phase4_transformation/
    ├── phase5_eda/
    ├── phase6_visualisations/
    └── phase7_modelisation/

    src/
    ├── __init__.py
    └── preprocessing.py

    requirements.txt
    CHANGELOG.md
    README.md

## Installation

Cloner le dépôt :

    git clone https://github.com/LhenryAxel/nba-next-season-points-ml.git
    cd nba-next-season-points-ml

Installer les dépendances :

    pip install -r requirements.txt

## Modèle sauvegardé

La pipeline Machine Learning complète est sauvegardée avec `joblib`.

Elle contient :

- gestion des valeurs manquantes ;
- standardisation des variables numériques ;
- encodage des variables catégorielles ;
- modèle Ridge final.

Exemple de chargement :

    import joblib

    model = joblib.load(
        "models/nba_pts_ridge_pipeline_v1_YYYYMMDD.joblib"
    )

    predictions = model.predict(X)

## Documentation

Le projet contient :

- un Data Dictionary couvrant les 251 colonnes ;
- une documentation des transformations ;
- les métadonnées du modèle ;
- un fichier `requirements.txt` ;
- un changelog ;
- les résultats des différentes phases.

## Limites

Le dataset supervisé contient uniquement les joueurs observés lors d'une saison N+1 consécutive.

Les retraites, sorties de ligue ou saisons entièrement manquées ne sont donc pas représentées par la cible.

Certaines informations potentiellement importantes ne sont pas explicitement modélisées :

- blessures ;
- changements de rôle ;
- contrats ;
- transferts ;
- changements d'entraîneur ;
- évolution de la rotation d'équipe.

Le modèle doit donc être considéré comme un outil d'estimation et non comme une prévision certaine.

## Auteur

Axel Lhenry