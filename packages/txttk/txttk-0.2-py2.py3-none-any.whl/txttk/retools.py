# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from collections import defaultdict, OrderedDict
from itertools import combinations
import re

def condense(ss_unescaped):
    """
    Given multiple strings, returns a compressed regular expression just
    for these strings

    >>> condense(['she', 'he', 'her', 'hemoglobin'])
    'he(moglobin|r)?|she'
    """
    def estimated_len(longg, short):
        return (3 
                + len(short) 
                + sum(map(len, longg)) 
                - len(longg) 
                * (len(short) - 1) 
                - 1 )
    
    def stupid_len(longg):
        return sum(map(len, longg)) + len(longg)
    
    ss = [re.escape(s) for s in set(ss_unescaped)]
    ss.sort(key=len)
    
    short2long = defaultdict(lambda: {'p':[],'s':[]})
    
    for short, longg in combinations(ss, 2):
        if longg.startswith(short):
            short2long[short]['p'].append(longg)
        if longg.endswith(short):
            short2long[short]['s'].append(longg)
    
    short2long = sorted(list(short2long.items()), 
                        key=lambda x: len(x[0]), 
                        reverse=True)
    
    output = []
    objs = set(ss)
    
    for s, pre_sur in short2long:
        pp = set(pre_sur['p']) & objs
        ss = set(pre_sur['s']) & objs
        if ((stupid_len(pp) - estimated_len(pp, s)) 
            < (stupid_len(ss) - estimated_len(ss, s))): 
            reg = (r'({heads})?{surfix}'
                    .format(surfix=s, 
                           heads='|'.join(sorted([p[:-len(s)] for p in ss], 
                           key=len, 
                           reverse=True))))
            assert len(reg) == estimated_len(ss, s)
            output.append(reg)
            objs -= (ss | set([s]))
        elif ((stupid_len(pp) - estimated_len(pp, s)) 
            > (stupid_len(ss) - estimated_len(ss, s))): 
            reg = (r'{prefix}({tails})?'
                .format(prefix=s, 
                        tails='|'.join(sorted([p[len(s):] for p in pp], 
                        key=len, 
                        reverse=True))))
            assert len(reg) == estimated_len(pp, s)
            output.append(reg)
            objs -= (pp | set([s]))

    for residual in objs:
        output.append(residual)
    return re.sub(r'\(([^)])\)\?', r'\1?', r'|'.join(output))