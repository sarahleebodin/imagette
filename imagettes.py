# In[Bibliothèques]

import geopandas
import rasterio
import os
import shutil
from random import shuffle
import numpy as np

# In[Paramètres]

nom_points = "points.shp"                      # Chemin vers l'image contenant les points
nom_image_raster = "image_multispectral.tif"   # Chemin vers l'image contenant les données raster
nom_dossier = "imagettes"                      # Chemin vers le dossier de sortie 
nom_dossier_entrainement = "entrainement"      # Nom du dossier entrainement
nom_dossier_validation = "validation"          # Nom du dossier validation
nom_colonne_classe = 'Desc'                    # Nom de la colonne contenant la classe du point
nombre_classes = 15                            # Nombre de classes différente 
taille_image = 128                             # Taille des imagettes en pixel
pourcentage_entrainement = 0.8                 # Pourcentage (de 0 à 1) pour l'entraînement  

# In[Chargement des données et création du dossier de sortie]

points = geopandas.read_file(nom_points)
image_raster = rasterio.open(nom_image_raster)
os.makedirs(nom_dossier, exist_ok=True)
os.makedirs(nom_dossier_entrainement, exist_ok=True)
os.makedirs(nom_dossier_validation, exist_ok=True)

# On crée une liste vide pour chaque classe pour y stocker les noms des imagettes par classe

liste_imagette_par_classe = []

for i in range(0, nombre_classes):

    liste_imagette_par_classe.append([])

# In[Découpage des imagettes]

nombre_points = np.shape(points)[0]                 # On récupère le nombre de points
tab_coordonnees = np.empty((nombre_points, 2))      # On crée un tableau vide pour stocker les coordonnées des points


# On récupère les coordonnées en x et y de tous les points du shapefile

for i in range(0,nombre_points):


    tab_coordonnees[i][0] = points.geometry.x[i]
    tab_coordonnees[i][1] = points.geometry.y[i]


image_raster = rasterio.open(nom_image_raster)         # On ouvre l'image raster
resolution_x, resolution_y = image_raster.res          # On récupère la résolution en x et y 


# Pour chaque point, on découpe une imagette

for i in range(0,nombre_points):

    # On calcule les coordonnées du découpage

    position_x = tab_coordonnees[i][0]
    position_y = tab_coordonnees[i][1]

    left = position_x - (taille_image / 2) * resolution_x
    right = position_x + (taille_image / 2) * resolution_x
    down = position_y - (taille_image / 2) * resolution_y
    up = position_y + (taille_image / 2) * resolution_y

    # On découpe

    carre = rasterio.windows.from_bounds(left, down, right, up, transform=image_raster.transform)
    imagette = image_raster.read(window=carre)

    # On enregistre

    classe = points[nom_colonne_classe][i]
    nom_imagette = f"imagette__{classe}_{i + 1}.tif"

    liste_imagette_par_classe[int(classe) - 1].append(nom_imagette)           # On ajoute le nom de l'imagette dans la bonne liste
    
    metadata = image_raster.meta.copy()                                 # On change les metadatas
    metadata.update({
            "height": imagette.shape[1],
            "width": imagette.shape[2],
            "transform": rasterio.transform.from_origin(left, up, resolution_x, resolution_y)
    })


    fichier_imagette = rasterio.open(f"{nom_dossier}/{nom_imagette}", 'w', **metadata)      # On sauvegarde l'imagette
    fichier_imagette.write(imagette)
    fichier_imagette.close()

image_raster.close()

# On fait la séparation validation / entraînement

for i in range(0, nombre_classes):

    shuffle(liste_imagette_par_classe[i])                                                                 # On mélange les noms pour une classe donnée
    nombre_imagette_entrainement = int(len(liste_imagette_par_classe[i]) * pourcentage_entrainement)        # On regarde combien on en prend pour l'entraînement 

    for j in range(0,len(liste_imagette_par_classe[i])):

        nom_imagette = liste_imagette_par_classe[i][j]

        if j < nombre_imagette_entrainement:

            shutil.copy(f"{nom_dossier}/{nom_imagette}", f"{nom_dossier_entrainement}/{nom_imagette}")

        else :

            shutil.copy(f"{nom_dossier}/{nom_imagette}", f"{nom_dossier_validation}/{nom_imagette}")
            