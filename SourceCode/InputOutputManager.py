
import os
import json

def getApplicationDirectory() -> str :
    """
    Répertoire racine dans lequel se situent
      le répertoire IN_Folder
      le répertoire OUT_Folder
    
    [Args]
      name (str): le code en 3 lettres la fonction demandée.
    
    [Returns]
      str : le repertoire.
    """
    startingDirectory = os.getcwd()
    index = startingDirectory.find("SourceCode")
    if index != -1 :
        return str(startingDirectory[:index-1])
    return startingDirectory
    
def getSourceFilename() -> str :
    """
    Nom du fichier source en json,
      contient l'arborescence source.
      Doit se trouver dans le répertoire IN_Folder
    
    [Returns]
      str : Nom du fichier source en json
    """
    return getApplicationDirectory() +"/IN_Folder/employes-data.json"

def getTargetFilename() -> str :
    """
    Nom du fichier modifié en json,
      contient l'arborescence modifiée
      avec le calcul des salaires mensuels.
      Doit se trouver dans le répertoire OUT_Folder
    
    [Returns]
      str : Nom du fichier modifié en json
    """
    return getApplicationDirectory() +"/OUT_Folder/jsonResult.json"

def getCsvFilename() -> str :
    """
    Nom du fichier csv,
      contient les salaires mensuels.
      Doit se trouver dans le répertoire OUT_Folder
    
    [Returns]
      str : Nom du fichier csv
    """
    return getApplicationDirectory() +"/OUT_Folder/result.csv"

def openData() -> dict:
    """
    Lit le fichier source en json qui se trouve 
      dans le répertoire IN_Folder
    
    [Returns]
      dict : la structure de donnée source
    """
    filename = getSourceFilename()

    data = None
    with open(filename, 'r') as file :
        data = json.load(file)

    if data == None :
       return { "Data count": 0 }
    
    return data

def saveToJson(data : dict):
    """
    Ecrit le fichier modifié en json,
      contient les salaires mensuels.
      Se trouve dans le répertoire OUT_Folder
    
    [Args]
      data (dict): la structure de donnée modifiée.
    """
    filename = getTargetFilename()
    
    jsonObject = json.dumps(data, indent=2)
    with open(filename, 'w') as file :
        file.write(jsonObject)

def saveToCSV(lines : list[str]) :
    """
    Ecrit le fichier csv,
      contient les salaires mensuels.
      Se trouve dans le répertoire OUT_Folder
    
    [Args]
      lines (list[str]): ensemble de lignes au format csv :
        ;  séparateur de cellule 
        \\n séparateur de ligne
    """
    filename = getCsvFilename()
    with open(filename, 'w') as file :
        file.writelines(lines)
    