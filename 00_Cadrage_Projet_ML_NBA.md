# Phase 0 — Cadrage du projet Machine Learning NBA

## 1. Informations générales

**Titre du projet :** Prévision de la performance offensive des joueurs NBA à la saison suivante

**Domaine :** Sport — Basketball — NBA Analytics

**Sujet précis :**  
Construire un modèle de régression capable de prédire le nombre de points par match d’un joueur NBA lors de la saison suivante, à partir de ses statistiques passées, de son évolution récente, de son rôle et du contexte de son équipe.

**Contexte / problématique :**  
Une franchise ou une cellule d’analyse souhaite anticiper l’évolution offensive de ses joueurs avant le début d’une nouvelle saison. Cette estimation peut aider à identifier les joueurs susceptibles de progresser ou de décliner, à attribuer les rôles offensifs et à évaluer l’impact de la concurrence au sein de l’effectif.

**Public cible :**  
Analystes NBA, recruteurs, responsables sportifs et staffs techniques.

**Moment de la prédiction :**  
La prédiction est réalisée juste avant le début de la saison N+1, lorsque les effectifs sont connus, mais avant que les statistiques de la saison N+1 existent.

**Période initiale :**  
Le dataset principal couvre les saisons 1996-97 à 2022-23. La période finale commune sera déterminée après vérification de la couverture des données complémentaires issues de l’API.

---

## 2. Questions business

| # | Question business | Impact potentiel |
|---|---|---|
| 1 | Quels indicateurs de la saison N distinguent les joueurs qui progressent ou régressent le plus en points par match lors de la saison N+1 ? | Identifier les profils de progression et de déclin. |
| 2 | Comment l’âge et l’expérience influencent-ils l’évolution du scoring d’une saison à l’autre ? | Anticiper les phases de développement, de pic et de déclin. |
| 3 | Dans quelle mesure le rôle actuel du joueur, temps de jeu, titularisations, volume de tirs et taux d’utilisation influence-t-il ses points futurs ? | Mieux attribuer les rôles et repérer les joueurs sous-utilisés. |
| 4 | La présence de coéquipiers à fort taux d’utilisation dans l’effectif de la saison suivante réduit-elle la progression offensive d’un joueur ? | Mesurer la concurrence pour les possessions et le ballon. |
| 5 | Pour quels profils le modèle commet-il les plus grosses erreurs : jeunes joueurs, vétérans, joueurs transférés ou joueurs ayant peu joué ? | Identifier les limites du modèle et les situations nécessitant une analyse humaine. |

---

## 3. Cadrage prédictif

**Question prédictive :**  
Peut-on prédire le nombre de points par match d’un joueur NBA lors de la saison N+1 à partir de ses statistiques jusqu’à la saison N et du contexte d’effectif connu avant le début de la saison N+1 ?

**Colonne cible officielle :**

```text
pts_next_season
```

Cette cible sera calculée à partir de la colonne `pts` de la saison suivante, après identification fiable des joueurs et vérification que les saisons sont consécutives.

**Type de problème :** Régression

**Métrique principale :** MAE — Mean Absolute Error

**Justification :**  
La MAE exprime directement l’erreur moyenne en points par match. Par exemple, une MAE de 2,3 signifie que le modèle se trompe en moyenne de 2,3 points par match.

**Métriques complémentaires :**

- RMSE, pour pénaliser davantage les grosses erreurs ;
- R², pour mesurer la part de variation expliquée.

**Baselines prévues :**

1. `DummyRegressor(strategy="mean")`, baseline obligatoire du cours ;
2. baseline métier : prédire que les points de la saison suivante seront égaux aux points de la saison actuelle.

**Répartition provisoire de la cible :**  
Lors d’une première construction basée sur les noms de joueurs, environ 9 895 transitions consécutives ont été trouvées. La cible possède une moyenne proche de 9,1 points, une médiane proche de 7,7 points et s’étend approximativement de 0 à 36,1 points. Ces valeurs devront être recalculées après ajout d’un véritable `player_id`.

**Extensions optionnelles, non officielles :**

```text
reb_next_season
ast_next_season
```

Les rebonds et les passes pourront être prédits en complément, mais `pts_next_season` reste l’unique cible principale pour respecter le cadre du guide.

---

## 4. Sources de données prévues

### Source 1 — Principale

- **Nom :** `all_seasons.csv`
- **Format :** CSV
- **Origine :** dataset NBA Players
- **Accès :** déjà téléchargé
- **Volume actuel :** 12 844 lignes et 22 colonnes brutes
- **Période :** 1996-97 à 2022-23
- **Contenu :** profil du joueur, équipe, âge, taille, poids, draft, matchs joués, points, rebonds, passes et statistiques avancées.

### Source 2 — Complémentaire

- **Nom prévu :** statistiques individuelles NBA
- **Format d’origine :** API / JSON
- **Objectif :** obtenir notamment `player_id`, `team_id`, position, minutes, volume de tirs et informations de rôle.
- **Accès et couverture historique :** à vérifier pendant la Phase 1.

### Source 3 — Enrichissement

- **Nom prévu :** effectifs et statistiques d’équipes NBA
- **Format d’origine :** API / JSON
- **Objectif :** récupérer les rosters, le contexte de l’équipe et construire des indicateurs agrégés de concurrence entre coéquipiers.
- **Accès et couverture historique :** à vérifier pendant la Phase 1.

---

## 5. Features envisagées

### Historique individuel

- points, rebonds et passes de la saison N ;
- moyenne des points sur les trois dernières saisons ;
- évolution des points ;
- ancienneté en NBA ;
- âge et âge au carré ;
- changement d’équipe.

### Rôle du joueur

- minutes par match ;
- taux de titularisation ;
- tentatives de tirs ;
- tentatives à trois points ;
- taux d’utilisation ;
- points par 36 minutes.

### Contexte de l’équipe

- rythme de l’équipe lors de la saison précédente ;
- offensive rating précédent de l’équipe ;
- meilleur taux d’utilisation parmi les coéquipiers ;
- somme des taux d’utilisation des trois coéquipiers principaux ;
- nombre de coéquipiers à forte utilisation ;
- concurrence au même poste.

Aucune information statistique produite pendant la saison N+1 ne sera utilisée comme feature.

---

## 6. Limites prévisibles

1. Le CSV principal ne contient pas de véritable `player_id`, ce qui pose un problème pour les homonymes.
2. La cible de points futurs n’existe que pour les joueurs présents en NBA lors de la saison suivante.
3. Le modèle ne pourra pas prévoir correctement certaines blessures, retraites ou décisions contractuelles absentes des données.
4. La couverture historique des positions, minutes, titulaires et rosters doit encore être vérifiée.
5. Les rookies sans saison NBA antérieure ne pourront pas être traités par le modèle principal.
6. Les styles de jeu et les règles ont évolué entre 1996 et 2023 ; l’effet de la saison devra être analysé.

---

## 7. Checklist de validation de la Phase 0

### Sujet et contexte

- [x] Domaine choisi
- [x] Sujet précis défini
- [x] Contexte et problématique rédigés
- [x] Public cible identifié
- [x] Moment réel de la prédiction défini

### Questions business

- [x] Cinq questions formulées
- [x] Questions spécifiques et mesurables
- [x] Impact potentiel indiqué

### Question prédictive

- [x] Question prédictive formulée
- [x] Cible nommée et calculable
- [x] Régression choisie
- [x] Métrique principale justifiée
- [x] Répartition provisoire examinée
- [x] Cible recalculée avec un véritable `player_id`
- [x] Dataset validé par le formateur

### Sources

- [x] Dataset principal déjà téléchargé
- [x] Deux sources complémentaires identifiées
- [x] Accessibilité et couverture de l’API vérifiées
- [ ] Période finale commune déterminée

### Faisabilité

- [x] Périmètre principal limité à une cible
- [x] Rebonds et passes conservés comme extensions
- [x] Risques de fuite de données identifiés
- [x] Utilisation de l’IA documentée

---

## 8. Décision de passage à la Phase 1

La Phase 0 est cadrée, mais deux validations restent obligatoires avant de considérer la checklist comme entièrement terminée :

1. validation du sujet et de la cible par le formateur ;  
2. vérification de la disponibilité et de la couverture des données NBA complémentaires.
