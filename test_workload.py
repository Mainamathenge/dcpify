import numpy as np

def heavy_math(n):
    # This should be detected as heavy
    result = 0
    for i in range(n):
        for j in range(n):
            result += np.dot(i, j)
    return result

def lightweight():
    # This should be ignored
    print("hello")
