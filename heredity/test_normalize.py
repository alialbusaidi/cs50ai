from heredity import normalize


# Define the people dict
people = {
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}

# Initialize probabilities values
probabilities = {
    person: {
        "gene": {
            2: 0,
            1: 0,
            0: 0
        },
        "trait": {
            True: 0,
            False: 0
        }
    }
    for person in people
}

# Manually assign probability before normalization
probabilities["Harry"]["trait"][True] = 0.1
probabilities["Harry"]["trait"][False] = 0.3


for person in people:
    print(f"{person}:")
    for field in probabilities[person]:
        print(f"  {field.capitalize()}:")
        for value in probabilities[person][field]:
            p = probabilities[person][field][value]
            print(f"    {value}: {p:.4f}")


# Use normalize function
normalize(probabilities)

# print results after normalization
for person in people:
    print(f"{person}:")
    for field in probabilities[person]:
        print(f"  {field.capitalize()}:")
        for value in probabilities[person][field]:
            p = probabilities[person][field][value]
            print(f"    {value}: {p:.4f}")
