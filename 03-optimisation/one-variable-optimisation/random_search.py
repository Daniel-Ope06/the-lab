import random
# import numpy
import math


# def f(x):
#     f = -x**6 + 28*x**5 - 307*x**4 + 1660*x**3 - 4564 * \
#         x**2 + 5872*x + 2688  # Change this for each question
#     return f

def f(x):
    return (math.sin(x) * math.cos(6*x))


# xbest = random.uniform(0, 10)
# fbest = f(xbest)
# steps = 100

# for i in range(1, steps):
#     xnew = random.uniform(0, 10)  # new random solution
#     fnew = f(xnew)
#     if fnew > fbest:
#         xbest = xnew
#         fbest = fnew

# print('xbest', xbest, 'fbest', fbest)


# Version 2
def random_search_2():
    for _ in range(10):
        xbest = random.uniform(0, 10)
        fbest = f(xbest)
        steps = 500

        for i in range(1, steps):
            xnew = random.uniform(0, 10)  # new random solution
            fnew = f(xnew)
            if fnew > fbest:
                xbest = xnew
                fbest = fnew

        print('xbest', xbest, 'fbest', fbest)


random_search_2()

# Q1
# xbest 1.3903672898291042 fbest 5482.14490302401

# Q2
# xbest 4.7119142812789985 fbest 0.9999958312272437
