# Imagettes

Production d'imagettes (patches) et séparation de celles-ci en deux jeux de données (entraînement et validation) pour la réalisation de classifications.

## Préparation

Installation de `geopandas`, `rasterio` et `numpy` (requirements.txt).

## Préparation données

Données nécessaires :
- GeoTif multispectral, par exemple, Sentinel-2, Landsat.
- Données vectorielles (points) étiquetées.

Assurez-vous que toutes les données sont dans le même dossier.

## Utilisation

### Paramètres à définir

| Paramètre  | Information |
| ------------- | ------------- |
| nom_points  | chemin vers le fichier comportant les données vectorielles (.shp)  |
| nom_image_raster  | chemin vers le fichier comportant l'image multispectrale (.tif)  |
| nom_dossier  | chemin vers le dossier de sortie  |
| nom_dossier_entrainement  | nom du dossier du jeu de données entraînement  |
| nom_dossier_validation  | nom du dossier du jeu de données validation  |
| nom_colonne_classe  | Nom de la colonne contenant la classe du point  |
| nombre_classes  | Nombre de classes différentes  |
| taille_image  | Taille des imagettes en pixel  |
| pourcentage_entrainement  | Pourcentage (de 0 à 1) pour l'entraînement    |

### Principe

Découpage des imagettes en fonction des points (récupération des coordonnées des points) et enregistrement des imagettes avec les noms des imagettes comportant la classe d'appartenance (important pour la suite).

Séparation des imagettes en deux jeux de données (entraînement et validation), en définissant le pourcentage (ex. 70%-30%) et en s'assurant que chaque classe est présente dans les deux (information dans le nom des imagettes).


### Exemple d'utilisation

Données utilisées :

![Capture d’écran 2024-10-04 195110](https://github.com/user-attachments/assets/356da0f1-10c6-434c-bbd2-8ed84dd9e0e5)

- 1 image multispectrale (5 bandes : R, G, B, Red Edge, NIR).
- Données vectorielles (points) étiquetées : 15 classes.

Exemple d'imagettes en sortie :

![des_imagettes](https://github.com/user-attachments/assets/56a7a1b3-0c7e-4bd6-9e2f-39ad9f74e727)

*128 x 128 pixels*
