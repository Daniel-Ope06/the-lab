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
#     xnew = xbest + random.gauss(0, 0.1)  # Hill climb step
#     fnew = f(xnew)
#     if fnew > fbest:
#         xbest = xnew
#         fbest = fnew

# print('xbest', xbest, 'fbest', fbest)

def hill_climb_2():
    for _ in range(10):
        xbest = random.uniform(0, 10)
        fbest = f(xbest)
        steps = 100

        for i in range(1, steps):
            xnew = xbest + random.gauss(0, 0.1)  # Hill climb step
            fnew = f(xnew)
            if fnew > fbest:
                xbest = xnew
                fbest = fnew

        print('xbest', xbest, 'fbest', fbest)


hill_climb_2()

# Q1
# xbest 4.901592491460627 fbest 5448.892101754391

# Q2
#
