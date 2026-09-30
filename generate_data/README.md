# Clustertool : préparation des données

## Conversion en json

Le fichier à traiter doit être un fichier json au même format que le fichier actuellement dans le répertoire **Data**, puis placé à la place de ce dernier.

## Génération des fichiers utiles

Adapter la ligne 3 du script *create_clusters.sh*

Lancer le script *create_data.sh* 

## Adaptation de l'API Flask

### Ajout des données

Une fois toutes les données obtenues, déplacer le corpus (fichier en *_corpus.json* dans **Data**) et le résultat du clustering (fichier dans **clustered_data**) dans le répertoire **clustertool\data**.
Puis copier les répertoires **motioncharts** et **streamcharts** dans **clustertool\frontend\templates** (ou copier leur contenu dans les répertoires correspondants s'il y a des données dans ces derniers que vous ne souhaitez pas perdre).

### Modification du code

Ajouter dans **clustertool\frontend\templates\clustering.html** ligne 36 une ligne permettant de sélectionner le nouveau corpus dans la liste déroulante.
