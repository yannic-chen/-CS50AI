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
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),
    Implication(And(AKnight, AKnave), AKnight),
    Implication(Not(And(AKnight, AKnave)), AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Implication(And(AKnave, BKnave), AKnight),
    Implication(Not(And(AKnave, BKnave)), AKnave),
    Implication(AKnight, BKnave),                   #If A tells the truth
    Implication(AKnave, BKnight)                    #If A lies
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Implication(And(AKnight, BKnight), AKnight),    #If A says truth
    Implication(And(AKnight, BKnight), BKnight),
    Implication(And(AKnave, BKnave), AKnight),
    Implication(And(AKnave, BKnave), BKnave),
    Implication(And(AKnight, BKnave), BKnight),     #If B says truth
    Implication(And(AKnight, BKnave), AKnight),
    Implication(And(AKnave, BKnight), BKnight),
    Implication(And(AKnave, BKnight), AKnave),
    Implication(AKnight, BKnight),                  #Who is the other if the claimer is a knight.
    Implication(BKnight, AKnave)

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Not(And(AKnight, AKnave)),                      #rules of the game
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Implication(Or(AKnight, AKnave), AKnight),      #If A is either a Knight or a Knave, then A is a Knight
    Implication(AKnave, BKnight),                   #If B tells the truth, that A is a knave, then B is a Knight
    Implication(Not(AKnave), BKnave),               #Otherwise B is a knave
    Implication(CKnave, BKnight),                   #If B tells the truth that C is a knave, then B is a knight
    Implication(Not(CKnave), BKnave),               #else B is a knave
    Implication(AKnight, CKnight),                  #if C tells the truth that A is a knight, then C is a knight
    Implication(Not(AKnight), CKnave)               #else C is a knave
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
