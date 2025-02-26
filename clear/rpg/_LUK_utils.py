def LUK2prob(LUK: int) -> float:
    return 10e-5 * (LUK ** 2)

def donate2LUK(donate: int):
    difficulty = 1381
    difficulty2 = 20
    return difficulty2 - (difficulty / (donate + (difficulty / (difficulty2 - 1))))