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


def month_to_int(month):
    """
    Takes input a month as string and returns a int representation, 0 through 11.
    """
    # Define dict to map months to an int
    month_map = {
    "Jan": 0,
    "Feb": 1,
    "Mar": 2,
    "Apr": 3,
    "May": 4,
    "Jun": 5,
    "Jul": 6,
    "Aug": 7,
    "Sep": 8,
    "Oct": 9,
    "Nov": 10,
    "Dec": 11,
}
    
    return month_map(month)

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        0 - Administrative, an integer
        1 - Administrative_Duration, a floating point number
        2 - Informational, an integer
        3 - Informational_Duration, a floating point number
        4 - ProductRelated, an integer
        5 - ProductRelated_Duration, a floating point number
        6 - BounceRates, a floating point number
        7 - ExitRates, a floating point number
        8 - PageValues, a floating point number
        9 - SpecialDay, a floating point number
        10 - Month, an index from 0 (January) to 11 (December)
        11 - OperatingSystems, an integer
        12 - Browser, an integer
        13 - Region, an integer
        14 - TrafficType, an integer
        15 - VisitorType, an integer 0 (not returning) or 1 (returning)
        16 - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Read file using open and reader method
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        # Initialize evidence and labels lists
        evidence, labels = [], []

        # Read data row by row, appending each data to the relevant list
        for row in reader:
            # Append to evidence the a list of data points from colum 0 to 17
            evidence.append(
                [
                    int(row[0]), float(row[1]), int(row[2]),
                    float(row[3]), int(row[4]), float(row[5])
                ]
                +
                [
                    float(cell) for cell in row[6:10]
                ]
                +
                [

                ]
            )

            # Append to labels labels for each row



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
