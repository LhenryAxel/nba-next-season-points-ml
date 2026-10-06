# Transformations du dataset NBA

## 1. Sources utilisées

Le projet combine plusieurs sources NBA API :

- biographie des joueurs ;
- statistiques individuelles de base ;
- statistiques individuelles avancées ;
- statistiques collectives de base ;
- statistiques collectives avancées ;
- rosters.

Un dataset Kaggle a également été étudié lors des premières phases mais n'a
pas été joint au dataset final en raison de l'absence de PLAYER_ID et du risque
d'ambiguïté lié aux homonymes.

## 2. Nettoyage

Les principales opérations de nettoyage sont :

- suppression des colonnes techniques inutiles ;
- harmonisation des types ;
- standardisation des unités physiques ;
- conservation des valeurs manquantes lorsqu'elles possèdent un sens métier ;
- création d'indicateurs de disponibilité ;
- absence de suppression arbitraire des outliers.

## 3. Jointures

Le grain final correspond à une ligne par joueur et par saison.

Les jointures utilisent principalement :

- PLAYER_ID ;
- SEASON ;
- TEAM_ID lorsque le contexte équipe est nécessaire.

## 4. Création de la cible

La cible `pts_next_season` correspond aux points par match du joueur lors de la
saison suivante.

Elle est créée uniquement lorsque la saison suivante est consécutive.

Les lignes ne possédant pas de saison N+1 consécutive ne font pas partie du
dataset supervisé.

## 5. Feature engineering

Les principales variables créées sont :

- statistiques de la saison précédente ;
- variations par rapport à la saison précédente ;
- moyennes historiques calculées uniquement sur le passé ;
- statistiques par minute ;
- ratios offensifs ;
- groupes d'âge ;
- groupes d'expérience ;
- indicateurs rookie ;
- indicateurs multi-équipe ;
- disponibilité des données roster.

## 6. Préparation Machine Learning

Les identifiants et colonnes non généralisables sont exclus des features.

Les variables numériques sont :

- imputées par la médiane ;
- standardisées avec StandardScaler.

Les variables catégorielles sont :

- normalisées pour les valeurs manquantes ;
- imputées par la modalité la plus fréquente ;
- encodées avec OneHotEncoder.

Toutes ces transformations sont intégrées dans la Pipeline Machine Learning.

## 7. Découpage temporel

Le dataset est séparé chronologiquement :

- train : 1996-97 à 2011-12 ;
- validation : 2012-13 à 2016-17 ;
- test : 2017-18 à 2021-22.

La validation croisée respecte également l'ordre temporel.

## 8. Limites

Le dataset supervisé contient uniquement les joueurs observés lors d'une saison
N+1 consécutive.

Les retraites, sorties de ligue et saisons entièrement manquées ne sont donc pas
représentées par la cible.

Les blessures, changements de rôle, contrats et certains mouvements d'effectif
ne sont pas explicitement modélisés.
