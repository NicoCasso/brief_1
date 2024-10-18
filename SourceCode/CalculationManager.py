
#Number of weeks in a month
def numberOfWeeksInAMonth() -> float:
    """
    Centralisation de la valeur à utiliser 
    pour convertir le salaire par semaine
    en salaire par mois.
    
    [Returns] 
    float: le nombre de semaines dans un mois.
    """
    return 4.0

#Available functions
#def getFunction(name:str) -> function :
def getFunction(name:str) :
    """
    Les fonctions utilisables dans cette application sont :\n
      maximum : max
      moyenne : avg
      médiane : med
      minimum : min
    
    [Args]
      name (str): le code en 3 lettres la fonction demandée.
    
    [Returns]
      function: une fonction lambda qui s'applique sur une liste.
    """
    if name == "avg" : return lambda x : round(100 * sum(x) / len(x))/100
    elif name == "min" : return lambda x : min(x)
    elif name == "med" : return lambda x : list(sorted(x))[len(x)//2]
    elif name == "max" : return lambda x : max(x)
    else : return lambda x : print(f"The {x} function is not implemented")

#Global or Enterprise specific operation
#def functionApply(operation: function, data : dict, subsidiaryName : str =None)-> float:
def functionApply(operation, data : dict, subsidiaryName : str =None)-> float:
    """
    Applique la fonction operation \n
      soit à la liste des employés de l'entreprise (subidiaryName)\n
      soit aux employés de toutes les entreprises si aucun paramètre n'est fourni (None) 
    
    [Args]
      operation (function): le code en 3 lettres la fonction demandée.
      data (dict): la donnée source (directement issue du json).
      subsidiaryName (str) : Optionnel, None par défaut, le nom de l'entreprise.
    
    [Returns] 
        float: le résultat de l'application de la fonction.
    """
    salaries = getSalaries(data, subsidiaryName)
    result = operation(salaries)
    return result

#Common functions
def getSalaries(data : dict, subsidiaryName : str) -> list:
    """
    Calcule les salaires mensuels des employés \n
      soit de l'entreprise (subidiaryName)\n
      soit de toutes les entreprises si aucun paramètre n'est fourni (None)
    
    [Args]
      data (dict): la donnée source (directement issue du json)
      subsidiaryName (str) : Optionnel , le nom de l'entreprise
    
    [Returns] 
      list: une liste de salaires mensuel.
    """
    source = {}
    if subsidiaryName == None :
        source = data
    else :
        source = { subsidiaryName : data[subsidiaryName] }
    
    salaries = []
    for subName, subEmps in source.items() :
        for empTuple in subEmps :
            salaries.append(getSalary(empTuple))
    
    return salaries

def getSalary(empDict : dict) -> float :
    """
    Calcule le salaire mensuel d'un seul employé.
    
    [Args]
      empDict (dict): la partie de la donnée source 
      qui ne concerne que cet employé
    
    [Returns]
      float: le salaire mensuel de cet employé.
    """
    empHourly_rate = int(empDict["hourly_rate"])
    empWeekly_hours_worked = int(empDict["weekly_hours_worked"])
    empContract_hours = int(empDict["contract_hours"])

    overtimeHours = empWeekly_hours_worked- empContract_hours
    overtimeHours = overtimeHours if overtimeHours>0 else 0

    contractHours = empWeekly_hours_worked - overtimeHours

    weekSalary = 0.0 
    weekSalary += float(contractHours*empHourly_rate)
    if overtimeHours>0 :
        weekSalary += float(overtimeHours*1.5*empHourly_rate)

    return numberOfWeeksInAMonth() * weekSalary

def getEmpWithSalary(empDict : dict) -> dict :
    """
    Calcule le salaires d'un seul employé.
    
    [Args] 
      empDict (dict): la partie de la donnée source 
      qui ne concerne que cet employé
    
    [Returns] dict: la donnée source avec une nouvelle paire "clé"/valeur : \n
      clé = "salary" / valeur = salaire calculé de l'employé
    """
    customEmp = empDict.copy()
    customEmp["salary"] = getSalary(empDict)
    return customEmp 

def getStatistics(data: dict, subsidiaryName : str) -> dict:
    """
    Calcule les statistiques pour une entreprise.
    
    [Args] 
    data (dict): les données sources.
    subsidiaryName (str) : le nom de l'entreprise.
    
    [Returns] 
    dict: max_salary average_salary median_salary min_salary
    """
    statistics = {}
    statistics["max_salary"] = functionApply(getFunction("max"), data, subsidiaryName)
    statistics["average_salary"] = functionApply(getFunction("avg"), data, subsidiaryName)
    statistics["median_salary"] = functionApply(getFunction("med"), data, subsidiaryName)
    statistics["min_salary"] = functionApply(getFunction("min"), data, subsidiaryName)
    return statistics

def getGlobalStatistics(data: dict) -> dict:
    """
    Calcule les statistiques pour toutes les entreprises.
    
    [Args]
    data (dict): les données sources.
    
    [Returns]
    dict: max_salary average_salary median_salary min_salary
    """
    statistics = {}
    statistics["max_salary"] = functionApply(getFunction("max"), data)
    statistics["average_salary"] = functionApply(getFunction("avg"), data)
    statistics["median_salary"] = functionApply(getFunction("med"), data)
    statistics["min_salary"] = functionApply(getFunction("min"), data)

    return statistics

def createModifiedData(sourceData : dict) -> dict:
    """
    Créé une nouvelle structure de données à partir des données initiales.

    [Args]
      data (dict): les données sources.
    
    [Returns]
      dict: exemple {
          "name": "GLOBAL",
          "statistics": { "max_salary": 0.0, "average_salary": 0.0, "median_salary": 0.0 "min_salary": 0.0 },
          "enterprises": [{
              "name": "Nom d'entreprise",
              "statistics": { "max_salary": 0.0, "average_salary": 0.0, "median_salary": 0.0 "min_salary": 0.0 },
              "employees": [{
                  "name": "Nom du salarié", "job": "fonctiondu salarié", "salary": 0.0 }
              ]}] 
      }
    """
    modifiedData = {}
    modifiedData["name"] ="GLOBAL"
    modifiedData["statistics"] = getGlobalStatistics(sourceData)
    
    allEnterprises = []
    for key, val in sourceData.items() :
        currentEnterprise = {}
        currentEnterprise["name"] = key
        currentEnterprise["statistics"] = getStatistics(sourceData, key)
        employees = []
        for empData in  sorted(map(lambda emp: getEmpWithSalary(emp), val), key=lambda emp : emp["salary"], reverse=True) :
            newEmpData = {}
            newEmpData["name"] = empData["name"]
            newEmpData["job"] = empData["job"]
            newEmpData["salary"] = empData["salary"]
            employees.append(newEmpData)

        currentEnterprise["employees"] = employees
        allEnterprises.append(currentEnterprise)

    modifiedData["enterprises"] = allEnterprises

    return modifiedData

            

