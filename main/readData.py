import pandas as pd
import numpy as np
import sys

def readFile(filename, n):
    """
    Reads the data in the file
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
            anharm.append(arr[i, 4]*2*np.pi*1e6)  # Transfer from [MHz] to angular frequency
            levels.append(int(arr[i, 5]))
    except Exception as error:
        print("Something is wrong with the csv file! Check the example-file in git for how it should look."
              " Remember to use correct separation of values")
        raise sys.exit(1)
    return relax, depha, therma, anharm, levels

def read_data(filename):
    """Function that reads qubit number from user and qubit parameters from a .csv file
    Maybe change what parameters come from the file? Separation in csv must be ;
    Easiest is to create an excel and save it as a csv with ;
    Also has error handling if csv file is wrong or if input is wack"""

    # Input for number of qubits
    cont = False
    while cont == False:
        n = input("\nEnter number of qubits (1 <= n <= 15): ")
        try:
            n = int(n)
            if 1 <= int(n) <= 15:
                n = int(n)
                cont = True
            else:
                print("You didn't enter an integer between 1 and 15!")
        except ValueError:
            print("That's not a whole number!")
    # Input for number of trajectories
    cont = False
    while cont == False:
        ntraj = input("\nEnter number of trajectories (no input => 500): ")
        if ntraj == (""):
            ntraj = 500
            cont = True
        else:
            try:
                ntraj = int(ntraj)
                if type(ntraj)==int:
                    cont = True
            except ValueError:
                print("That's not a whole number. Try again!")

    # Read the file
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
            anharm.append(arr[i, 4]*2*np.pi*1e6)  # Transfer from [MHz] to angular frequency
            levels.append(int(arr[i, 5]))
    except Exception as error:
        print("Something is wrong with the csv file!")
        raise sys.exit(1)
    return n, ntraj, relax, depha, therma, anharm, levels


## Troubleshooting
if __name__ == "__main__":
    n, ntraj, relax, depha, therma, anharm, levels = read_data()
