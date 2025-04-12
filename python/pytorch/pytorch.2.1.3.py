# -*- coding=utf-8 -*-

import math

import numpy


def softmax(inMatrix):
    """Softmax用以解决概率计算中概率结果大而占绝对优势的问题。例如函数计算结果中的两个值a和b，且a>b，如果简单地以值的大小为单位来衡量，那么在后续的使用过程中，a永远被选用，而b由于数值较小而不会被选择，但是有时也需要使用数值小的b，Softmax就可以解决这个问题。

       [numpy.mat() function](https://www.w3resource.com/numpy/array-creation/mat.php)
        The numpy.mat function is used to interpret the input as a matrix, and if necessary, convert it to a matrix. It returns a matrix from a string, nested sequence, or array-like object.

        The math.exp() method returns E raised to the power of x (Ex).
    'E' is the base of the natural system of logarithms (approximately 2.718282) and x is the number passed to it.
    """
    m, n = numpy.shape(inMatrix)
    print(f"inMatrix shape: {m}, {n}")
    outMatrix = numpy.mat(numpy.zeros((m, n)))
    soft_sum = 0
    for idx in range(0, n):
        outMatrix[0, idx] = math.exp(inMatrix[0, idx])
        soft_sum += outMatrix[0, idx]
    print(f"{outMatrix=}")
    for idx in range(0, n):
        outMatrix[0, idx] = outMatrix[0, idx] / soft_sum

    print(f"return {outMatrix=}")
    return outMatrix


a = numpy.array([[1, 2, 1, 2, 1, 1, 3]])
print(f"{a=}")
print(f"{softmax(a)=}")
