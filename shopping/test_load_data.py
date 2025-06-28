import sys
from shopping import load_data 

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])

    print(f"First evidence: {evidence[0]}")
    print(f"first label: {labels[0]}")