from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # A is either a knight or knave 
    Or(AKnight, AKnave),
    # A can't be both
    Not(And(AKnight, AKnave)),
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave),

    # A can't be both
    Not(And(AKnight, AKnave)),

    # B can't be both
    Not(And(BKnight, BKnave)),

    # A says "We are both knaves"
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    # A is either a knight or knave 
    Or(AKnight, AKnave),
    # B is either a knight or knave 
    Or(BKnight, BKnave),

    # A can't be both
    Not(And(AKnight, AKnave)),

    # B can't be both
    Not(And(BKnight, BKnave)),

    # A says "We are the same kind."
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # B says "We are of different kinds."
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO

    # A is either a knight or knave 
    Or(AKnight, AKnave),
    # B is either a knight or knave 
    Or(BKnight, BKnave),
    # C is either a knight or knave 
    Or(CKnight, CKnave),
    # A can't be both
    Not(And(AKnight, AKnave)),

    # B can't be both
    Not(And(BKnight, BKnave)),

    # C can't be both
    Not(And(CKnight, CKnave)),

    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Or(And(Implication(AKnight, AKnight), Implication(AKnave, AKnave)),
        And(Implication(AKnight, AKnave)), Implication(AKnave, AKnight)),
    
    Implication(BKnight, 
                And(Implication(AKnight, AKnave), 
                    Implication(AKnave, AKnight))),
    Implication(BKnave, Not(And(Implication(AKnight, AKnave), 
                        Implication(AKnave, AKnight)))),
    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
