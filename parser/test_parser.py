from parser import *

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

s = "Holmes sat at home."

s = preprocess(s)

trees = list(parser.parse(s))

for tree in trees:
        tree.pretty_print()
        print(f'Tree label: {tree.label()}')
        print(f'tree[0]: {tree[0]}')
        print(f'tree[1]: {tree[1]}')
        for sub in tree.subtrees():   
            print(f'Sub: {sub}')
            print(f'Sub leaves: {sub.leaves()}')
        print(f'Leaves: {tree.leaves()}')
        print(f'Height: {tree.height()}')
        print('')