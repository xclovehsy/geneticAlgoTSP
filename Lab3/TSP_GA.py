#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: 徐聪
# datetime: 2022-05-07 17:07
# software: PyCharm

import math
import random
import matplotlib.pyplot as plt
import numpy as np
from GA import GA
import pandas as pd


class TSP(object):
    def __init__(self, life_count):
        self.life_count = life_count  # 种群数量
        self.city_count = -1  # 基因长度即城市的数量
        self.cities = None  # 城市的经纬度数据
        self.history_distance = []
        self.best_distance = -1

        self.init_city()  # 初始化数据

        self.ga = GA(aCrossRate=0.6,
                     aMutationRage=0.1,
                     aLifeCount=self.life_count,  # 种群数量
                     aGeneLenght=self.city_count + 1,  # 基因长度即城市的数量+1
                     aMatchFun=self.matchFun())

    def init_city(self):
        """
        初始化城市数据
        :return:
        """
        self.cities = pd.read_csv("cities.csv")  # 各个城市经纬度数据
        self.city_count = self.cities.shape[0]  # 城市数量

    def distance(self, order):
        """
        获取顺序的总路径长度
        :param order: 旅行城市顺序
        :return:
        """
        dis = 0.0  # 路径长度
        # print(order)
        for i in range(0, len(order) - 1):
            dis += self.get_dis(order[i], order[i + 1])

        return dis

    def get_dis(self, city1_index, city2_index):
        """
        获取两个城市之间的路径长度
        :param city1_index:
        :param city2_index:
        :return:
        """
        # 获取城市一二的经纬度数据
        city1_x, city1_y = self.cities.iloc[city1_index]['latitude'], self.cities.iloc[city1_index]['longitude']
        city2_x, city2_y = self.cities.iloc[city2_index]['latitude'], self.cities.iloc[city2_index]['longitude']

        dis = math.sqrt((city1_x - city2_x) ** 2 + (city1_y - city2_y) ** 2)
        return dis

    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)  # 适配值——距离的倒数

    def draw_image(self, order):
        """
        绘制旅行图像
        :param order: 旅行顺序
        :return:
        """
        x = self.cities['latitude']
        y = self.cities['longitude']
        txt = self.cities['city']

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.figure(figsize=(15, 10), dpi=80)

        plt.scatter(x, y, s=50, c='b')
        for i in range(len(x)):
            plt.annotate(txt[i], xy=(x[i], y[i]), xytext=(x[i] + 0.1, y[i] + 0.1))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标

        for i in range(len(order) - 1):
            # print()
            # print()
            plt.plot([x[order[i]], x[order[i + 1]]], [y[order[i]], y[order[i + 1]]], 'r')

        plt.xlabel("latitude")
        plt.ylabel("longitude")
        plt.title("The shortest route to all cities")
        plt.grid()
        plt.show()

    def distance_figure(self):
        """
        绘制distance迭代图像
        :return:
        """
        plt.figure(figsize=(20, 8), dpi=80)
        y = self.history_distance
        x = np.arange(len(self.history_distance))
        plt.plot(x, y)
        plt.ylabel('distance')
        plt.xlabel('iteration')
        plt.title("Variation of path distance with iteration")
        plt.grid()
        plt.show()

    def run(self, gen_cnt):
        """
        运行遗传算法
        :param gen_cnt: 迭代次数
        :return:
        """
        cnt = 0
        while cnt < gen_cnt:
            cnt += 1
            self.ga.next_generation()
            distance = self.distance(self.ga.best.gene)

            self.history_distance.append(distance)
            print(f"gen:{cnt}, dis:{distance}")

        self.best_distance = self.distance(self.ga.best.gene)  # 获取最短路径长度

        # 打印迭代结果
        print("=====运行结果======")
        print(f"经历过{gen_cnt}次迭代后，最短路径为：")
        way = self.ga.best.gene
        for i in range(len(way) - 1):
            print(
                f"{self.cities['city'][way[i]]}——>{self.cities['city'][way[i + 1]]},  dis:{round(self.get_dis(way[i], way[i + 1]) * 10000) / 10000}")
        print(f"最短路径距离为：{round(self.best_distance * 10000) / 10000}")


def main():
    tsp = TSP(20)
    tsp.run(200)
    tsp.distance_figure()
    # order = [2, 9, 1, 0, 7, 6, 5, 4, 3, 8, 2]
    tsp.draw_image(tsp.ga.best.gene)


if __name__ == '__main__':
    main()
