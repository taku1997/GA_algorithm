# coding: utf-8
import random
import bisect
import numpy as np
from matplotlib import pyplot




N_ITEMS = 15 #アイテムの個数
CROSSOVER_PROB = 0.8 #交叉率
MUTATE_PROB = 0.05 #突然変異率
MAX_WEIGHT = 75 #ナップサックの重量
INDIVIDUAL = 10 #個体数

#アイテム
apple = {'value': 2, 'weight': 3}
bento = {'value': 8, 'weight': 8}
water_bottle = {'value': 10, 'weight': 6}
handkerchief = {'value': 6, 'weight': 2}
clothes = {'value': 16, 'weight': 16}
ball = {'value': 5, 'weight': 5}
sweets = {'value': 3, 'weight': 2}
game_machine = {'value': 6, 'weight': 4}
wallet = {'value': 10, 'weight': 3}
ski = {'value': 30, 'weight': 25}
pc = {'value': 40, 'weight': 35}
smartphone = {'value': 15, 'weight': 10}
pencil_case =  {'value': 5, 'weight': 5}
book = {'value': 3, 'weight': 6}
speaker =  {'value': 8, 'weight': 7}
kleenex = {'value': 5, 'weight': 3}

towel = {}
item = 0

max_array = []
ave_array = []

class GA:
    def __init__(self):
        #初期値設定
        self.items = [apple,bento,water_bottle,handkerchief,clothes,ball,sweets,game_machine,wallet,ski,pc,smartphone,book,speaker,kleenex]
        self.choice_item = {}
        self.fitness = [None for _ in range(INDIVIDUAL)]
        self.expected_value = [None for _ in range(INDIVIDUAL)]
        self.C_sum = [None for _ in range(INDIVIDUAL)]
        self.V_sum = [None for _ in range(INDIVIDUAL)]
        self.weight_all = 0
        self.individual = [[0] * N_ITEMS for i in range(INDIVIDUAL)]
        self.nextE = [[0] * N_ITEMS for i in range(INDIVIDUAL)]

    def main(self):
        threshold = 0
        count = 0
        self.generate_individual()
        for i in range(20):
            max,threshold = self.evaluation()
            self.select_items()
            self.crossover()
            self.mutate()
            
            count = count + 1
            max_array.append(max)
            ave_array.append(threshold)

        #グラフを作成
        pyplot.plot(np.arange(1,count+1), max_array, label='max')
        pyplot.plot(np.arange(1,count+1), ave_array, label='average') 
        #グラフの軸
        pyplot.xlabel('Generation')
        pyplot.ylabel('Fitness')
        pyplot.legend()
        pyplot.show()

    #個体の生成
    def generate_individual(self):
        for i in range(INDIVIDUAL):
            for j in range(N_ITEMS):
                self.individual[i][j] = random.randint(0, 1)

    #適応度評価
    def evaluation(self):
        for i in range(INDIVIDUAL):
            self.C_sum[i] = 0.0
            self.V_sum[i] = 0.0
            for j in range(N_ITEMS):
                item = self.items[j]
                if self.individual[i][j] == 1:
                    self.C_sum[i] = item["weight"] + self.C_sum[i]
                    self.V_sum[i] = item["value"] + self.V_sum[i]
                if self.C_sum[i] > MAX_WEIGHT:
                    self.V_sum[i] = 0
        print("総重量:",self.C_sum)
        print("総価値:",self.V_sum)
        #print("最大適応度:",max(self.V_sum))
        #print("平均適応度:",sum(self.V_sum)/len(self.V_sum))
        return max(self.V_sum),sum(self.V_sum)/len(self.V_sum)


    #選択手法・ルーレット選択
    def select_items(self):
        for i in range(INDIVIDUAL):
            total = sum(self.V_sum)
            c_sum = np.cumsum(self.V_sum)
            self.choice_item[i] = bisect.bisect_left(c_sum, total * random.random())
            #print(self.choice_item[i])
        
        for j in range(INDIVIDUAL):
            for k in range(N_ITEMS):
                self.nextE[j][k] = self.individual[self.choice_item[j]][k]
            #print(self.nextE[j])

    #交叉手法・単純交叉
    def crossover(self):
        for h in range(5):
            value = random.random()
            index1 = random.randint(0,INDIVIDUAL-1)
            index2 = random.randint(0,INDIVIDUAL-1)
            if value < CROSSOVER_PROB:
                r1 = random.randint(0,N_ITEMS)
                r2 = random.randint(r1,N_ITEMS)
                childA = [0] * N_ITEMS 
                childB = [0] * N_ITEMS
                for i in range(N_ITEMS):
                    if r1<=i and i<=r2:
                        childA[i] = self.nextE[index1][i]
                        childB[i] = self.nextE[index2][i]
                    else:
                        childA[i] = self.nextE[index2][i]
                        childB[i] = self.nextE[index1][i]

                for j in range(N_ITEMS):
                    self.nextE[index1][j] = childA[j]
                    self.nextE[index2][j] = childB[j]
                # print("返還後")
                # print(childA)
                # print(childB)
                # print("------")


    #突然変異
    def mutate(self):
        #突然変異を起こす
        value = random.random()
        index = random.randint(0,INDIVIDUAL-1)
        for i in range(N_ITEMS):
            if value < MUTATE_PROB:
                self.nextE[index][i] = self.bit_inversion(self.nextE[index][i])
        
        for j in range(INDIVIDUAL):
            for k in range(N_ITEMS):
                self.individual[j][k] = self.nextE[j][k]

    #bitの反転
    def bit_inversion(self,value):
        #print("突然変異実施")
        if value == 0:
            return 1
        else:
            return 0



if __name__ == "__main__":
    GA().main()