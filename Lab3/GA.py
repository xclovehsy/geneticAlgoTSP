#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: 徐聪
# datetime: 2022-05-07 16:55
# software: PyCharm

import random

from life import Life


class GA(object):
    """
    遗传算法类
    """

    def __init__(self, aCrossRate, aMutationRage, aLifeCount, aGeneLenght, aMatchFun=lambda life: 1):
        self.croessRate = aCrossRate  # 交叉概率
        self.mutationRate = aMutationRage  # 突变概率
        self.lifeCount = aLifeCount  # 种群数量，就是每次我们在多少个城市序列里筛选，这里初始化为100
        self.geneLenght = aGeneLenght  # 其实就是城市数量+1
        self.matchFun = aMatchFun  # 适配函数
        self.lives = []  # 种群
        self.best = None  # 保存这一代中最好的个体
        self.generation = 1  # 一开始的是第一代
        self.crossCount = 0  # 一开始还没交叉过，所以交叉次数是0
        self.mutationCount = 0  # 一开始还没变异过，所以变异次数是0
        self.bounds = 0.0  # 适配值之和，用于选择是计算概率

        self.init_life()

    def init_life(self):
        """
        初始化种群
        :return:
        """
        for i in range(self.lifeCount):
            new_gene = [x for x in range(self.geneLenght - 1)]
            random.shuffle(new_gene)  # 打乱基因
            new_gene.append(new_gene[0])  # 需要回到原点
            new_life = Life(new_gene)
            self.lives.append(new_life)  # 将新的个体添加到种群

        # for i in range(5):
        #     print(self.lives[i].gene)

    def judge(self):
        """
        计算该种群中每一个个体的适配值
        :return:
        """
        self.bounds = 0.0
        self.best = self.lives[0]  # 假定第一个为最优个体

        for life in self.lives:
            life.score = self.matchFun(life)
            self.bounds += life.score

            if self.best.score < life.score:  # 如果该个体的适配值大于最优个体，则替代
                self.best = life

    def cross(self, parent1, parent2):
        """
        基因交叉
        :param parent1: 父代1
        :param parent2: 父代2
        :return: 子代的基因形
        """
        index1 = random.randint(0, self.geneLenght - 2)
        index2 = random.randint(index1, self.geneLenght - 2)
        temp_gene = parent2.gene[index1:index2]  # 获取父代2中的基因片段
        new_gene = []

        cnt = 0
        for g in parent1.gene[0:self.geneLenght - 1]:
            if cnt == index1:
                # new_gene.append(temp_gene)
                for g2 in temp_gene:
                    new_gene.append(g2)

                cnt += 1

            if g not in temp_gene[0:self.geneLenght - 1]:
                new_gene.append(g)
                cnt += 1

        new_gene.append(new_gene[0])  # 添加起始节点
        self.crossCount += 1  # 突变个体数量加一
        return new_gene

    def mutation(self, parent_gene):
        """
        基因突变
        :param parent_gene: 父代的基因
        :return: 子代的基因
        """
        new_gene = parent_gene[0:self.geneLenght-1]
        index1, index2 = random.randint(0, self.geneLenght - 2), random.randint(0, self.geneLenght - 2)
        # print(self.geneLenght)

        new_gene[index1], new_gene[index2] = new_gene[index2], new_gene[index1]
        new_gene.append(new_gene[0])
        self.mutationCount += 1
        return new_gene

    def get_one(self):
        """
        轮盘赌获取种群中的个体
        :return:
        """
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life

        return self.lives[len(self.lives) - 1]

    def new_child(self):
        """
        根据父代种群生成一个新的个体
        :return: 新个体
        """
        parent1 = self.get_one()  # 随机获取一个父代
        new_gene = parent1.gene[:]  # 子代的基因

        rate1 = random.random()  # 是否进行基因交叉
        if rate1 <= self.croessRate:
            parent2 = self.get_one()  # 随机获取第二个父代
            new_gene = self.cross(parent1, parent2)

        rate2 = random.random()  # 是否进行基因突变
        if rate2 <= self.mutationRate:
            new_gene = self.mutation(new_gene)

        return Life(new_gene)

    def next_generation(self):
        """
        繁衍新一代种群
        :return:
        """
        self.judge()  # 计算父代种群个体的适配值

        new_lives = [self.best]  # 用于存储新一代种群，并将父代种群中适配值最高的个体加入新的种群

        while len(new_lives) < self.lifeCount:
            new_lives.append(self.new_child())

        self.lives = new_lives
        self.generation += 1  # 种群代数加一
