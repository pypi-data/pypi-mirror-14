# -*- coding: utf-8 -*-
#列表数组相关的函数


def strip_duplicate_from_list(ls):
    '''从列表中去除重复数据'''
    return sorted(set(ls),key=ls.index)
