import nltk
import sys
from nltk.tokenize import word_tokenize

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP NP | SS
SS -> S Conj S
NP -> N | Det N | Det Adj N | Det Adj Adj N | Det Adj Adj Adj N | NP Conj NP | PP
VP -> V | Adv V | V Adv | V PP | V NP | Adv V NP
PP -> P NP | NP P NP | P NP Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Use word_tokenize to create list of words, and store in temp variable
    words = word_tokenize(sentence)

    word_list = list()

    # Iterate over all words/characters in list and:
    for word in words:
        # exclude nonalphabets
        if word.isalpha():
        # lowecase them, and add to list
            word_list.append(word.lower())

    # return resultant list
    return word_list



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = list()
    for sub in tree.subtrees(lambda t: t.label() == "NP"):
        # Check if this NP contains any other NP subtrees (excluding itself)
        has_nested_np = False
        for child in sub.subtrees():
            if child != sub and child.label() == "NP":
                has_nested_np = True
                break
        
        if not has_nested_np:
            chunks.append(sub)

    return chunks

if __name__ == "__main__":
    main()
