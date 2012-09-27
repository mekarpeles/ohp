#-*- coding: utf-8 -*-

"""
   ohp
   ~~~
   A collection of interview questions
   1) performing outer_joins on csv files
   2) least square regression

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import csv
import random
import string
from operator import add
from itertools import product
import numpy, scipy

def csv_parse(csvf):
    """Reads a csv file into memory and parses its contents into a
    dict containing keys and values
    """
    f = open(csvf, 'r')
    csv_fields = f.readline().strip().split(',')
    csv_records = [r.split(',') for r in f.read().split('\n')]
    f.close()
    return {'keys': csv_fields, 'values': csv_records}

def outer_join(csvs=['data/employees.csv', 'data/teams.csv'], on=None,
               operator="left", saveas="output/tmp.csv"):
    """Performs an <operator> outer join over csv1 and csv2 according
    to the on clause.

    params:
        csvs - a list (of cardinality > 2) of csv filepaths
        on - the name of the key common to both tables
        operator - the type of outer join
        saveas - logs join output csv to a tmp file (overwrites, doesn't append)

    >>> outer_join(on='position')
    ['name,passwd,gender,age,boss,members,position,id',
     '0,Brian,JEE56FSB5VW,female,22,engineering,2,engineering,Akeem,39',
     '1,Chaim,YJD23QTT7OV,male,10,marketing,0,marketing,Simon,27', 
     ...
     ]
    """
    def verify_constraints_satisfied():
        try:
            assert(len(csvs) > 1)
        except:
            raise IndexError("At least 2 .csv files are required for a join")

    def greedy_match_key(tbl, key, value):
        """Greedily searches within a table for the first occurrence
        of a value under the 'key' column and returns the row it is
        found under, minus the column designated by the 'key'.

        >>> greedy_match_key([['id', 'name'], [[0, 'mek'], ['1', 'chris']]],
        ...                  'name', 'mek')
        [0]
        """
        if key in tbl['keys']:
            index = tbl['keys'].index(key)
            for row in tbl['values']:
                if row[index] == value:
                    return row
        return ['w'] * (len(tbl['keys']) - 1)

    def log(rows):
        with open(saveas, 'w') as f:            
            f.write('\n'.join('\n'.join(row) for row in rows))
        
    def left_join(tbls):
        """Returns the result of performing a left outer join on the
        pivot table and all other tables involved in the join. The
        return type is a list of lists, each outmost list representing
        a table row and each inner most list representing a keyed
        value
        """
        joined_keys = list(set(reduce(lambda tbl_a, tbl_b: tbl_a + tbl_b,
                                      (tbl['keys'] for tbl in tbls))))
        rows = [joined_keys]
        pivot = tbls[0]
        if on in pivot['keys']:
            key_index = pivot['keys'].index(on)
            for row in pivot['values']:
                tmp_row = row
                join_value = row[key_index]
            
                for tbl in tbls[1:]:
                    if on in tbl['keys']:
                        match = greedy_match_key(tbl, on, join_value)
                        if match:
                            tmp_row += match
                rows.append(tmp_row)
        return rows
        
    verify_constraints_satisfied()
    tbls = map(csv_parse, csvs)
    output = left_join(tbls)
    print output
    log(output)
    return output

def sqrt(n2, precision=5):
    """Newton's Iterative method for calculating square root:
    O(precision), linear
    """
    def approx(x): return round(x, precision)
    n = 1
    while not approx(n**2) == approx(n2):
        n = .5 * (n + (n2/n))
    return approx(n)

def mergesort(lst):
    """O(n*log n)"""

    def merge(left, right):
        """O(log n), consider using deque because it outperforms lists
        when a lot of popping is needed.
        """
        result = []
        while len(left) and len(right):
            if left[0] < right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left)
        result.extend(right)
        return result

    if len(lst) <= 1: return lst        
    midpoint = len(lst)/2
    left, right = mergesort(lst[:midpoint]), mergesort(lst[midpoint:])
    return merge(left, right)

def lslr(dataset='data/xy.csv'):
    """Shell for least squares regression"""
    def residual_sums():
        pass

    def slr(xs, ys, xys):
        """Simple linear regression"""
        samples = len(data['values'])
        sum_x = sum(xs)
        sum_y = sum(ys)
        sum_yx = sum(float(x) * float(y) for x, y in xys)
        sum_x2 = sum(float(x) * float(x) for x in xs)
        sum_y2 = sum(float(y) * float(y) for y in ys)
        mean_x = sum_x / samples
        mean_y = sum_y / samples
        slope = (sum_yx - ((sum_x * sum_y)/samples)) / (sum_x2 - ((sum_x * sum_x) / samples))
        y_intercept = mean_y - (slope * mean_x)

        # correlation coefficient 
        r = sum_yx / sqrt(sum_x2 * sum_y2)
        return "slope: {}, y-intercept: {}, r: {}".format(slope, y_intercept, r)
    
    data = csv_parse(dataset)
    xys = data['values']
    xs = [float(x) for x, y in xys]
    ys = [float(y) for x, y in xys]              
    #falls back to simple linear regression
    return slr(xs, ys, xys)

if __name__ == "__main__":    
    print outer_join(on='position')
    print lslr()
