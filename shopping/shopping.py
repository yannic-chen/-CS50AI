import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # loading data, given the filename. Using csv reader function and then converting to list
    csv_file = open(filename)
    reader = csv.reader(csv_file)
    data = list(reader)

    #seperating the data to evidence and label.
    label = []
    evidence = []
    for row in data[1:]:                #looping through all rows, except the header
        if row[-1] == "TRUE":             #append the last item of the row (i.e. last column)
            label.append(int(1))        #converting bool to int
        elif row[-1] == "FALSE":
            label.append(int(0))
        evidence.append(row[:-1])       #append all but the last item of the row (all columns except last)

    #converting evidence to numerical
    for row in evidence:
        row[6] = float(row[6])
        row[7] = float(row[7])
        #convert month
        if row[10] == "Jan":
            row[10] = int(0)
        elif row[10] == "Feb":
            row[10] = int(1)
        elif row[10] == "Mar":
            row[10] = int(2)
        elif row[10] == "Apr":
            row[10] = int(3)
        elif row[10] == "May":
            row[10] = int(4)
        elif row[10] == "June":
            row[10] = int(5)
        elif row[10] == "Jul":
            row[10] = int(6)
        elif row[10] == "Aug":
            row[10] = int(7)
        elif row[10] == "Sep":
            row[10] = int(8)
        elif row[10] == "Oct":
            row[10] = int(9)
        elif row[10] == "Nov":
            row[10] = int(10)
        else:
            row[10] = int(11)
        #convert Visitor Type
        if row[15] == "Returning_Visitor":
            row[15] = int(1)
        else:
            row[15] = int(0)
        #convert Weekend
        if row[16] == "TRUE":
            row[16] = int(1)
        else:
            row[16] = int(0)
        #convert rest to float and int
        row[0] = int(row[0])
        row[1] = float(row[1])
        row[2] = int(row[2])
        row[3] = float(row[3])
        row[4] = int(row[4]) 
        row[5:10] = map(float, row[5:10])
        row[11:15] = map(int, row[11:15])
        #convert to tuple and return
        refined = tuple((evidence, label))

    return refined
    
def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    Kmodel = KNeighborsClassifier(n_neighbors = 1)
 
    fitted = Kmodel.fit(evidence, labels)

    return fitted



def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    sensitivity_correct = 0
    specificity_correct = 0

    sensitivity_real = labels.count(1)
    specificity_real = labels.count(0)

    for i in list(zip(predictions, labels)):                        #zip combines each index of two lists together to form a tuple. This is then converted to a list of tuple using list()
        # for each tuple in the list, calling set(i) returns the set of unique numbers: {0,1} or {0} or {1}
        if set(i) == {1}:                                           #if both numbers in the tuple are 1, set(i) will return {1}
            sensitivity_correct += 1
        elif set(i) == {0}:
            specificity_correct += 1
    
    sensitivity = sensitivity_correct / sensitivity_real
    specificity = specificity_correct / specificity_real

    return tuple((sensitivity, specificity))

if __name__ == "__main__":
    main()
