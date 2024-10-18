def getMaxEmpLen(data : dict, fieldName : str) -> int:
    """
    Obtient la longueur maximum 
      atteinte par les valeurs (sous forme de string) 
      du champ fieldName 

    [Args]
      data (dict): la structure de donnée source.
      fieldName (str): le champ recherché.
    
    [Returns]
    str : la longueur maximum atteinte par une valeur de ce champ.
    """
    maxLength=0
    for subsidiary, content in data.items() :
        for empDict in content :
            stringValue = str(empDict[fieldName])
            if len(stringValue) > maxLength :
                maxLength = len(stringValue)

    return maxLength

def fillWithSpaces(content : str, maxLength : int) -> str :
    """
    Ajoute des espaces à une chaine de caractères
      jusqu'à la longueur désirée (maxLength)
    
    [Args]
      content (str): la chaine de caractères à formatter.
      maxLength (int): la longueur voulue
    
    [Returns]
      str : une chaine de caractère de longueur maxLength
    """
    result = content
    while len(result) < maxLength :
        result += " "
    
    return result

def createCsvLines(data : dict) -> list[str] :
    """
    Crée les lignes du fichier csv 
      à partir de la structure de donnée modifiée.
      contient les statistiques par entreprise,
      contient les salaires mensuels.
    
    [Args]
      data (dict): la structure de donnée modifiée.
    
    [Returns]
      list[str]: ensemble de lignes au format csv :
        ;  séparateur de cellule 
        \\n séparateur de ligne
    """
    lines = []
    for enterprise in data["enterprises"] :

        statisticsLines =[]
        statisticsLines.append(";Statistiques des salaires pour l'entreprise {0}:;".format(enterprise["name"]))
        statisticsLines.append(";Salaire moyen:;{0:.2f}€;".format(enterprise["statistics"]["average_salary"]))
        statisticsLines.append(";Salaire le plus élevé:; {0:.2f}€;".format(enterprise["statistics"]["max_salary"]))
        statisticsLines.append(";Salaire le plus bas:; {0:.2f}€;".format(enterprise["statistics"]["min_salary"]))

        lines.append("Entreprise: {0}\n".format(enterprise["name"]))
        lines.append("\n")
        lines.append("Nom;Fonction;Salaire mensuel;{0}\n".format(statisticsLines[0]))
        empCount = 0
        for empData in enterprise["employees"] :
            
            currentLine = "{0};{1};{2:.2f}€;".format(empData["name"], empData["job"],empData["salary"])
            if empCount < 3 : 
                currentLine+=(statisticsLines[empCount+1])

            empCount+=1

            lines.append(currentLine+"\n")

        lines.append("\n")

    return lines
