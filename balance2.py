from sympy import Matrix, lcm
import re


def run(reactants, products):
    reactants = reactants.replace(' ', '').split("+")
    products = products.replace(' ', '').split("+")
    elementList = []
    elementMatrix = []

    def addToMatrix(element, index, count, side):
        # If elementMatrix needs new row
        if index == len(elementMatrix):
            elementMatrix.append([])  # add the new row
            for i in elementList:
                # Fill new row with the same amount of 0's as elements we have
                elementMatrix[index].append(0)
        # If the element is not in our list yet,
        if element not in elementList:
            elementList.append(element)  # then let's add it to our list
            # thus we need to add an extra zero to each row of the matrix
            for i in range(len(elementMatrix)):
                elementMatrix[i].append(0)
        # The column of our matrix (& list) on which the element lies
        column = elementList.index(element)
        elementMatrix[index][column] += count*side

    def findElements(word, index, multiplier, side):
        elementWithNumber = re.split('([A-Z][a-z]?)', word)
        i = 0
        while i < len(elementWithNumber) - 1:
            i += 1
            if len(elementWithNumber[i]) > 0:
                # if we got a polyatomic do this stuff to get the right element counts
                if elementWithNumber[i+1].isdigit():
                    count = int(elementWithNumber[i+1])*multiplier
                    addToMatrix(elementWithNumber[i], index, count, side)
                    i += 1
                else:  # otherwise just do normal stuff
                    addToMatrix(elementWithNumber[i], index, multiplier, side)

    def interpretCompound(compound, index, side):
        # Splits 'bits' of compounds ex: (NH4)3PO4 goes to ['', '(NH4)3', 'PO4']
        bits = re.split('(\([A-Za-z0-9]*\)[0-9]*)', compound)
        for bit in bits:
            if bit.startswith("("):  # If its a polyatomic
                # Split polyatomic from its multiplier
                # (NO3)3 goes to ['(NO3', '3', '']
                bit = re.split('\)([0-9]*)', bit)
                # gets the multiplier of the polynomial
                multiplier = int(bit[1])
                bit = bit[0][1:]  # strips the first parentheses
            else:
                multiplier = 1
            findElements(bit, index, multiplier, side)

    for i in range(len(reactants)):
        interpretCompound(reactants[i], i, 1)
    for i in range(len(products)):
        interpretCompound(products[i], i + len(reactants), -1)

    # Manipulates our matrix into a solution set of coefficients
    # transposes to columns of compounds, rows of elements
    elementMatrix = Matrix(elementMatrix).transpose()
    # finds the solution to the matrix
    solution = elementMatrix.nullspace()[0]
    mult = lcm({i.q for i in solution})
    solution = mult * solution
    solutionList = solution.tolist()

    out = ""
    for i in range(len(reactants)):
        out += str(solutionList[i][0])+reactants[i]
        if i < len(reactants)-1:
            out += " + "
    out += " --> "
    for i in range(len(products)):
        out += str(solutionList[i+len(reactants)][0]) + products[i]
        if i < len(products)-1:
            out += " + "

    return out
