# -*- coding: utf-8 -*-
'''
Created on 2012-10-5
@author: Administrator
'''
from collections import defaultdict
import itertools
import time
import gc
import operator
import profile

gc.disable()

a = [
[ 8, 0, 0, 0, 0, 0, 0, 0, 0 ], 
[ 0, 0, 3, 6, 0, 0, 0, 0, 0 ], 
[ 0, 7, 0, 0, 9, 0, 2, 0, 0 ], 
[ 0, 5, 0, 0, 0, 7, 0, 0, 0 ], 
[ 0, 0, 0, 0, 4, 5, 7, 0, 0 ], 
[ 0, 0, 0, 1, 0, 6, 0, 3, 0 ], 
[ 0, 0, 1, 0, 0, 0, 0, 6, 8 ],  
[ 0, 0, 8, 5, 0, 0, 0, 1, 0 ], 
[ 0, 9, 0, 0, 0, 0, 4, 0, 0 ]  
#        0, 1, 2, 3,|4, 5, 6,|7, 8
     ]
#a = [
#        [ 0, 7, 0, 0, 0, 0, 0, 0, 0], #0
#        [ 5, 0, 3, 0, 0, 6, 0, 0, 0], #1
#        [ 0, 6, 2, 0, 8, 0, 7, 0, 0], #2
#        #
#        [ 0, 0, 0, 3, 0, 2, 0, 5, 0], #3
#        [ 0, 0, 4, 0, 1, 0, 3, 0, 0], #4
#        [ 0, 2, 0, 9, 0, 5, 0, 0, 0], #5
#        #
#        [ 0, 0, 1, 0, 3, 0, 5, 9, 0], #6
#        [ 0, 0, 0, 4, 0, 0, 6, 0, 3], #7
#        [ 0, 0, 0, 0, 0, 0, 0, 2, 0], #8
##        0, 1, 2, 3,|4, 5, 6,|7, 8
#     ]

a = [
        [0,0,2,4,5,0,7,0,0]
       ,[0,4,0,0,0,8,0,3,0]
       ,[8,0,1,0,0,3,5,0,6]
       ,[0,5,3,0,0,0,0,0,4]
       ,[7,0,0,0,0,0,0,0,2]
       ,[2,0,0,0,0,0,6,7,0]
       ,[3,0,6,5,0,0,1,0,7]
       ,[0,2,0,1,0,0,0,5,0]
       ,[0,0,7,0,2,9,4,0,0]
            ]




#a = [
#        [0, 0, 0, 0, 0, 0, 0, 0, 0], #0
#        [0, 0, 0, 0, 0, 0, 0, 0, 0], #1
#        [0, 0, 0, 0, 0, 0, 0, 0, 0], #2
#        #
#        [0, 0, 0, 0, 0, 0, 0, 0, 0], #3
#        [0, 0, 0, 0, 0, 0, 0, 0, 0], #4
#        [0, 0, 0, 0, 0, 0, 0, 0, 0], #5
#        #
#        [0, 0, 0, 0, 0, 0, 0, 0, 0], #6
#        [0, 0, 0, 0, 0, 0, 0, 0, 0], #7
#        [0, 0, 0, 0, 0, 0, 0, 0, 0], #8
##        0, 1, 2, 3,|4, 5, 6,|7, 8
#     ]

#===============================================================================
# 得到坐标点和值，相当于稀疏矩阵:(X,Y):value
#===============================================================================
exists_d = dict(((h_idx, y_idx), v) 
                for h_idx, y in enumerate(a) 
                for y_idx , v in enumerate(y)  if v)


h_exist = defaultdict(dict)
v_exist = defaultdict(dict)

#===============================================================================
# 二维数组
#===============================================================================
for k, v in exists_d.iteritems():
    h_exist[k[0]][k[1]] = v
    v_exist[k[1]][k[0]] = v

#===============================================================================
# 生成所有的组合
#===============================================================================
permutations = tuple(itertools.permutations(range(1, 10), 9))

h_d = {}

now = time.time()

#===============================================================================
# 取得行号与该行符合条件的组合
#===============================================================================
for hk, hv in h_exist.iteritems():
    
    #===========================================================================
    # 过滤横向，x轴与同行已知的点的值重复的组合
    #===========================================================================
    q = filter(lambda x:all((x[k] == v 
                             for k, v in hv.iteritems())), permutations)
    
    #===========================================================================
    # 过滤纵向，Y轴与同列已知的点的值重复的组合
    #===========================================================================
    q = filter(lambda x:all((x[vk] != v 
                             for vk , vv in v_exist.iteritems() 
                             for k, v in vv.iteritems() 
                             if k != hk)), q)
    
    h_d[hk] = q

#===============================================================================
# 不全某行没有任何提示
#===============================================================================
for line_idx in range(0, 9):
    if line_idx not in h_d:
        h_d[line_idx] = permutations

print time.time() - now 

def filter_by_column(y, resource_dict):
    '''@summary: 纵向过滤重复的值
    @param y: 待检测的一行排列
    @param resource_dict: 列序号及组合在对应列号的值列表
    '''
    if not resource_dict:
        return 1
    return all((y[k] not in  v for k, v in resource_dict.iteritems()))

sudokus = []

def check_3_lines(f, s, t):
    '''@summary: 检测3行的每三列是不是符合条件
    @param f: first line
    '''
    if len(set((f[0], f[1], f[2], s[0], s[1], s[2], t[0], t[1], t[2]))) != 9:
        return 1
    if len(set((f[3], f[4], f[5], s[3], s[4], s[5], t[3], t[4], t[5]))) != 9:
        return 1
    if len(set((f[6], f[7], f[8], s[6], s[7], s[8], t[6], t[7], t[8]))) != 9:
        return 1
    return 0

def check_2_lines(f, s):
    '''@summary: 检测两行数据的每三列是不是有重复值，提前淘汰有重复值的组合
    @param f: first line
    '''
    if len(set((f[0], f[1], f[2], s[0], s[1], s[2]))) != 6:
        return 1
    if len(set((f[3], f[4], f[5], s[3], s[4], s[5]))) != 6:
        return 1
    if len(set((f[6], f[7], f[8], s[6], s[7], s[8]))) != 6:
        return 1
    return 0

def solve_sudoku(h_d, h_idx=None, reserves=None
                 , solves=None, resource_dict=None):
    '''
    @param reserves: 已经验证过符合条件的排列
    @param solves: 最终的解决方案集合
    @param resource_dict: dict key in range(1,10),values 是每行同一列的数字的列表
    '''
    if solves is None:
        solves = []
    
    if h_idx is None :
        h_idx = 0
    for l0 in h_d[h_idx]:
        if reserves == None:
            _reserves = [l0, ]
            solve_sudoku(h_d, h_idx + 1, _reserves, solves)
        else:
            if not filter_by_column(l0, resource_dict):
                continue
            if h_idx in (1 , 4, 7):
                if check_2_lines(reserves[h_idx - 1], l0):
                    continue
            elif h_idx in (2, 5, 8) :
                if check_3_lines(reserves[h_idx - 2], reserves[h_idx - 1], l0):
                    continue
                    
            _reserves = list(reserves)
            _reserves.append(l0)
            if h_idx < 8:
                solve_sudoku(h_d, h_idx + 1, _reserves, solves
                             , dict((idx, set([i[idx] for i in _reserves])) 
                                    for idx in range(0, 9)))
            if h_idx == 8:
                solves.append(_reserves)
                print u"calc No. {num} result".format(num=len(solves))
                print u"*" * 50
                for i in solves[-1]:
                    print i
                
    else:
        if h_idx == 0:
            return solves
                
if __name__ == '__main__':
#(8, 7, 9, 1, 2, 3, 4, 6, 5)
#(5, 4, 3, 7, 9, 6, 2, 1, 8)
#(1, 6, 2, 5, 8, 4, 7, 3, 9)
#(7, 1, 8, 3, 4, 2, 9, 5, 6)
#(9, 5, 4, 6, 1, 8, 3, 7, 2)
#(3, 2, 6, 9, 7, 5, 8, 4, 1)
#(6, 8, 1, 2, 3, 7, 5, 9, 4)
#(2, 9, 7, 4, 5, 1, 6, 8, 3)
#(4, 3, 5, 8, 6, 9, 1, 2, 7)

    now = time.time()
    x = solve_sudoku(h_d)
    print time.time() - now

#    profile.run(u"solve_sudoku(h_d)", filename=r"d:\test.txt")
#    import pstats
#    p = pstats.Stats(r"d:\test.txt")
#    p.sort_stats("time").print_stats()

