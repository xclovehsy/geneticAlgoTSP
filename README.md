# geneticAlgoTSP
遗传算法解决旅行商问题


## 1. 项目描述

一个旅行者需要到国内的10个城市旅行，各城市的坐标见cities.csv文档。请设计一个合理的线路使旅行者所行的路程之和最小。注意：每个城市只能访问一次，且最后要回到原来出来的城市。



## 2. 算法思路

**遗传算法**是一种模仿自然界生物进化机制的全局搜索和优化方法。其具有以下几个基本的特征，接下来是对各个特征详细的说明。

- **表现型：**旅行依次经过的城市，即旅行的路径。例如“重庆—>北京—>上海—>天津—>成都—>… —>重庆”这是一种旅行路径，这里需要注意的是最终需要回到起点。

- **基因型：**我根据cities.csv文件中的城市出现的顺序，对城市进行1.2.3….编码。然后旅行经过的城市依次以序号进行编码。同时因为最后要回到起点，因此起点和终点的序号应该相同。

- 这里我们根据cities.csv文件中城市的次序进行编码，即：北京-0、天津-1、上海-2、重庆-3、拉萨-4、乌鲁木齐-5、银川-6、呼和浩特-7、南宁-8、哈尔滨-9。

- **编码：**这里我选择的编码方式为：对城市进行1.2.3…次序编码，然后一条旅行路线为一个个体，编码方式为起点到终点依次经过城市的序号编码。 

- **进化：**种群逐渐适应生存环境，即总的路径长度不断得到缩小。旅行线路的进化是以种群的形式进行的。

- **适应度：**度量某个旅行线路对于生存环境的适应程度。这里我使用旅行线路总的路径长度倒数作为种群的适应度

- **选择：**以一定的概率从种群中选择若干个个体。我使用轮盘赌的方式对种群中的个体进行选择。

- **交叉：**两个旅行线路的某一相同位置处城市编码，前后两串分别交叉组合形成两个新的旅行线路。也称基因重组或杂交；

- **变异：**以一定的概率对种群中的个体进行基因突变，即随机选择个体基因中两个城市的编号进行交换。 





## 3. 遗传算法步骤

开始循环直至找到满意的解。

1. 评估每条染色体所对应个体的适应度。
2. 遵照适应度越高，选择概率越大的原则，从种群中选择两个个体作为父方和母方。
3. 抽取父母双方的染色体，进行交叉，产生子代。
4. 对子代的染色体进行变异。
5. 重复2，3，4步骤，直到新种群的产生。

结束循环。

 

**算法流程图：**

![img](https://xc-figure.oss-cn-hangzhou.aliyuncs.com/img/202209072116751.gif)



## 4. 程序代码

这里一共有三个模块分别是Life.py、GA.py、TSP.py，每个模块的作用如下：

- Life.py为种群中的旅游线路个体类，里面包含旅行路线的基因型以及适应值
- GA.py为遗传算法内，里面主要包含了遗传算法的一些函数，例如基因交叉、基因突变、轮盘赌选择个体、生成个体、生成新一代种群等函数。
- TSP.py为旅行商问题的主要运行模块，包含对城市数据的读取，计算适应值、绘制适应度函数的进化曲线和最终选择的线路图等功能。

具体代码请查看目录“lab3”



## 5. 运行结果

这里设置一个种群中包含20个体，迭代200次后计算得出最优路径。gen表示迭代到第i代种群，dis表示该种群中最优个体的总旅行距离。

**运行结果如下：**

gen:1, dis:150.1067758288992

gen:2, dis:150.1067758288992

...

gen:199, dis:109.98824625831303

gen:200, dis:109.98824625831303

---

经历过200次迭代后，最短路径为：

北京——>呼和浩特, dis:4.8935

呼和浩特——>银川, dis:5.8709

银川——>乌鲁木齐, dis:19.0424

乌鲁木齐——>拉萨, dis:14.1505

拉萨——>重庆, dis:15.4347

重庆——>南宁, dis:6.9833

南宁——>上海, dis:15.5932

上海——>哈尔滨, dis:15.4157

哈尔滨——>天津, dis:11.5217

天津——>北京, dis:1.0825

最短路径距离为：109.9882

![img](https://xc-figure.oss-cn-hangzhou.aliyuncs.com/img/202209072119886.gif)

图2适应度函数的进化曲线

![img](https://xc-figure.oss-cn-hangzhou.aliyuncs.com/img/202209072119894.gif)

图3最终选择的线路图



## 6. 结果分析

由适应度函数的进化曲线可得知，刚开始种群进化速度很快，当适应值接近最优值时进化速度放缓。由图像可知在接近100代种群时适应值收敛。说明遗传的收敛效果良好。
