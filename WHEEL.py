import numpy as np
import numpy.random as r
import datetime
import random


class Wheel:
    ep = 0.0  # privacy budget epsilon
    d = 0  # domain size + maximum subset size
    m = 0  # maximum subset size
    p = 0.0  # coverage parameter
    user_num=1
    trate = 0.0  # hit rate when true
    frate = 0.0  # hit rate when false
    normalizer = 0.0  # normalizer for proportional probabilities
    covertime=0.0

    def __init__(self, d, m, ep,User_Num,p=None):
        self.ep = ep
        self.d = d
        self.m = m
        self.p = p
        self.user_num=User_Num
        self.__setparams()
    def __setparams(self):
        if self.p == None:
            self.p = self.bestCoverage(self.m, self.ep)
        self.normalizer = self.m * self.p * np.exp(self.ep) + (1 - self.m * self.p) * 1.0
        self.trate = self.p * np.exp(self.ep) / self.normalizer
        self.frate = self.p

    @staticmethod
    def bestCoverage(m, ep):
        p = 1.0 / (m * np.exp(ep) + 2 * m - 1)
        return p

    def coreRandomizer(self, xs, seed=None):
        z = 0.0
        if seed == None:
            seed=random.randint(0,self.user_num)*(self.d+self.m)
        cover = datetime.datetime.now()
        bs = int(np.ceil(1 / self.p))
        left = [0.0] * bs
        right = [0.0] * bs
        for b in range(0, bs):
            left[b] = min((b + 1) * self.p, 1.0)
            right[b] = b * self.p
        for x in xs:
            r.seed(seed + x)
            v = r.random()
            right[0] = max(v + self.p - 1.0, right[0])
            b = int(np.ceil(v / self.p)) - 1
            left[b] = min(v, left[b])
            if b + 1 < bs:
                right[b + 1] = max(v + self.p, right[b + 1])
        rightleast = right[0]
        for b in range(0, bs - 1):
            left[b] = max(left[b], right[b])
            right[b] = right[b + 1]
        b = bs - 1
        left[b] = max(left[b], right[b])
        right[b] = rightleast + 1
        l = np.sum(np.array(right) - np.array(left))
        self.covertime += (datetime.datetime.now() - cover).microseconds
        ur = random.random()
        a = 0.0
        for b in range(0, bs):
            a += np.exp(self.ep) * (right[b] - left[b]) / self.normalizer
            if a > ur:
                z = right[b] - (a - ur) * self.normalizer / np.exp(self.ep)
                break
            a += (self.normalizer - l * np.exp(self.ep)) * (left[(b + 1) % bs] + np.floor((b + 1) * self.p) - right[b]) / ((1.0 - l) * self.normalizer)
            if a > ur:
                z = left[(b + 1) % bs] - (1.0 - l) * self.normalizer * (a - ur) / (self.normalizer - l * np.exp(self.ep))
                break
        return (z, seed)

    def randomizer(self, xs, seed=None):
        z, seed = self.coreRandomizer(xs, seed)
        return self.recorder(z % 1.0, seed)

    # 从1到“d”开始遍历，在范围内的就置1
    def recorder(self,z, seed):
        pub = np.zeros((self.d), dtype=int)
        for i in range(1, self.d):
            r.seed(seed + i)
            v = r.random()
            if (v <= z and z < v + self.p) or (0 <= z and z < v + self.p - 1.0):
                pub[i] = 1
        return pub

    #进行校正，n为用户数量
    def decoder(self, hits, n):
        fs = np.array([(hits[i] - n * self.frate) / (self.trate - self.frate) for i in range(0, self.d)])
        return fs
    #测均方误差，从1到max,len(True_Value_List)=max+1
    def MSE(self,Noisy_Vaule_List,True_Value_List,User_num):
        result=0
        for i in range(1,len(True_Value_List)):
            tmp=abs(True_Value_List[i]/User_num-Noisy_Vaule_List[i]/User_num)
            result+=tmp*tmp
        result /=len(True_Value_List)-1
        return result
