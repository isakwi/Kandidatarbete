import pandas as pd
import sys

def readFile(filename, n):
    """
    Reads the data in the file qubitData.csv
    Input:
    - filename = name of file to be read
    - n = number of qubits (rows of paramaters in the file to be read)
    Output: data in the file
    (Qubit data: relax, depha, therma, anharm, levels)
    """
    relax = []
    depha = []
    therma = []
    anharm = []
    levels = []
    try:
        data = pd.read_csv(filename, sep=";")
        arr = data.to_numpy()
        for i in range(0, n):
            relax.append(arr[i, 1])
            depha.append(arr[i, 2])
            therma.append(arr[i, 3])
            anharm.append(arr[i, 4])
            levels.append(int(arr[i, 5]))
    except Exception as error:
        print("Something is wrong with the csv file! Check the example-file 'qubitData.csv' for how it should look."
              " Remember to use correct separation of values")
        raise sys.exit(1)
    return relax, depha, therma, anharm, levels


