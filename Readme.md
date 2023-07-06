Ce repo contient l'application de nos TDs de cours sur la classification d'information.

Dépendances : python3, typing-extensions
```py
pip install -m requirements.txt
```

Les fichiers suivants sont des main exécutables à lancer dans leur dossier respectif : 
```py
python3 monte_carlo_main.py
```
|fichier|dossier|résultats|
|----|----|----|
|distance_movies.py|recommandation|recommande des films à Toby, trouve les films similaires à Superman avec les distances de pearson et euclidienne|
|monte_carlo_main|combinatoire|la descente de gradiant sur le dataset de vol, trouve le minimum local sur un vol pris au hasard|
|annealing_main|combinatoire|applique le recul simulé sur un vol pris au hasard : non fonctionnel|
|genetic_main|combinatoire|applique des méthodes de sélection naturelle pour trouver la meilleure combinaison de vols|
|clustering_main|clustering|rassemble les articles les plus proches par paires en s'appuyant sur la distance de pearson appliquée sur leurs similitudes de mots|

Dans clustering main la sortie du programme est un fichier tree.json qui sert d'entrée au fichier script.js
Vous pouvez afficher le graphique en lançant un serveur local dans le dossier clustering
```
python3 -m http.server
```
Le graphique suivant s'affichera dans votre navigateur port 8000 `http://localhost:8000/`

