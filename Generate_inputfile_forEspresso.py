# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:     TDNF
# Purpose:  Generate input file for Espresso
# Author:   Huina Li
# Created:  28-02-2024
# Version:  1st
#-------------------------------------------------------------------------------
from sage.all import *
from copy import copy, deepcopy
from sage.rings.polynomial.pbori.pbori import *
from sage.rings.polynomial.pbori import *
from sympy.logic import SOPform
from sympy import symbols
import numpy as np

def int2bin(a: int, n: int) -> str:
    """int转二进制

    Args:
        a (int): 输入
        n (int): 输出比特数

    Returns:
        str: 输出
    """
    return "{0:b}".format(a).rjust(n,"0")

def generate_input_for_Espresso(W: list, n: int) -> str:
    """根据Espresso支持的输入文件格式，生成字符串

    Args:
        W (list): SAC论文中的W输入
        n (int): W的长度

    Returns:
        str: 输出字符串，Espresso格式
    """
    # Espresso格式的开头
    res = ".i " + str(n) + "\n"
    res += ".o 1\n"
    res += ".ilb "
    for i in range(n):
        res += "x" + str(i) + " "
    res += "\n"
    res += ".ob F\n"

    # Espresso格式的真值表
    res += generate_truthtable_for_Espresso(W, n)

    # Espresso格式的结尾
    res += ".e\n"
    return res

def generate_truthtable_for_Espresso(W: list, n: int) -> str:
    """根据Espresso格式和SAC论文，生成真值表对应的字符串

    Args:
        W (list): SAC论文中的W输入
        n (int): W的长度

    Returns:
        str: 输出真值表字符串，Espresso格式
    """
    # 生成2**n * n的矩阵，矩阵行从00...0到11...1
    entry = []
    for i in range(2**n):
        tmp=list(int2bin(i, n))
        listkey=[int(x) for x in tmp]
        entry.append(listkey)
    entry = np.mat(entry).T

    # 根据SAC论文计算W*entry
    w1= np.mat(W)
    y_binary = []
    tmp = np.array(w1*entry)
    for i in tmp[0]:
        if i > 0:
            y_binary.append(1)
        else:
            y_binary.append(0)

    # 根据计算结果获取真值表
    res = ""
    for i in range(len(y_binary)):
        # 只取y_binary数组中，0对应的下标
        if y_binary[i] == 0:
            line = int2bin(i, n)
            res += line + " 1\n"
    return res

def str2file(s: str, file_name: str):
    """字符串输入到新文件

    Args:
        s (str): 输入字符串
        file_name (str): 文件名
    """
    with open(file_name, "w") as f:
        f.write(s)

def main():
    W = [[10,-1,3,-5,8,-2,5,-1,-3,0,2,4,-10,1,-3,5]]
    # W = [[10,-1,3,-5]]
    n = len(W[0])
    file_name = "/home/user/lhn/SAC_ntu/sac_W_n" + str(n)
    res = generate_input_for_Espresso(W, n)
    str2file(res, file_name)

if __name__ == "__main__":
    main()
