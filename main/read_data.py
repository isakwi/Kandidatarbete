import pandas as pd


def read_data():
    """Function that reads qubit number from user and qubit parameters from a .csv file
    Maybe chang what parameters come from the file? Separation in csv must be ;
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

    # Read the file
    relax = []
    depha = []
    inter = []
    therma = []
    levels = []
    try:
        data = pd.read_csv("qubit_data.csv", sep=";")
        arr = data.to_numpy()
        for i in range(0, n):
            relax.append(arr[i, 1])
            depha.append(arr[i, 2])
            inter.append(arr[i, 3])
            therma.append(arr[i, 4])
            levels.append(int(arr[i, 5]))
    except:
        print("Something is wrong with the csv file!")
        quit()
    return n, relax, depha, inter, therma, levels


## Troubleshooting
if __name__ == "__main__":
    n, relax, depha, inter, therma, levels = read_data()
