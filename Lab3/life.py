#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: 徐聪
# datetime: 2022-05-07 16:53
# software: PyCharm

SCORE_DEFAULT = -1


class Life(object):
    def __init__(self, gene=None):
        self.gene = gene
        self.score = SCORE_DEFAULT
