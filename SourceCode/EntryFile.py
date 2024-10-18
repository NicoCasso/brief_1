
import os
if os.getcwd().count("SourceCode") == 0 :
    import SourceCode.InputOutputManager as iomg
    import SourceCode.CalculationManager as cmg
    import SourceCode.PresentationManager as pmg
else :
    import InputOutputManager as iomg
    import CalculationManager as cmg
    import PresentationManager as pmg

#def MainFunction() -> Generator[str]:
def MainFunction() :
    """
    Point d'entrée du programme,\n
    Fonction principale
    
    [Returns]
      Generator[str]: un nouveau str à chaque événement de l'application.
    """
    print(f"Starting from {os.getcwd()}")
    indent = "    "

    yield "{0}Root of IN_Folder and OUT_Folder : {1}".format(indent, iomg.getApplicationDirectory())
    yield "{0}Opening {1} ...".format(indent, iomg.getSourceFilename())

    sourceData = None
    try: sourceData = iomg.openData()
    except: yield "{0} ! error while opening source data".format(indent)

    targetData = None
    try: targetData = cmg.createModifiedData(sourceData)
    except: yield "{0} ! error while creating modified data".format(indent)

    yield "{0}Saving new data to {1} ...".format(indent, iomg.getTargetFilename())

    try: iomg.saveToJson(targetData)
    except: yield "{0} ! error while saving data to json".format(indent)

    yield "{0}Creating csv presentation ...".format(indent)

    lines = None
    try : lines = pmg.createCsvLines(targetData)
    except : yield "{0} ! error while creating csv lines".format(indent)

    yield "{0}Saving presentation to {1} ...".format(indent, iomg.getCsvFilename())

    try: iomg.saveToCsv(lines)
    except: yield "{0} ! error while saving csv file".format(indent)
    yield "Done."

if __name__ == "__main__" :
    for info in MainFunction() :
        print(info)