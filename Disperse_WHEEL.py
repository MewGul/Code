#枚举型WHEEL
import numpy as np
import math
import random
import numpy.random as r
class Disperse_Wheel:
    eps = 0.0
    d = 0.0
    m = 0.0
    g = 0.0
    p = 0.0
    q = 0.0
    user_num=0
    trate = 0.0
    frate = 0.0
    normalizer = 0.0

    def __init__(self, eps, d, m, User_NUM,g=None):
        self.ep = eps
        self.d = d
        self.m = m
        self.g = g
        self.user_num=User_NUM
        self.setparams()

    # 设置参数,这里g为改进后的值
    def setparams(self):
        g_tmp = int(round(self.m + self.m * np.exp(self.ep) / 2 + math.sqrt(self.m * self.m * np.exp(self.ep * 2) / 4 + 2 * self.m * self.m * np.exp(self.ep) - 2 * self.m * np.exp(self.ep))))
        self.g = g_tmp
        self.p = np.exp(self.ep) / (self.m * np.exp(self.ep) + g_tmp - self.m)
        self.q = 1 / (self.m * np.exp(self.ep) + g_tmp - self.m)
        self.trate = self.p
        self.frate = 1 / self.g

    # 核心扰动
    def CoreRandomizer(self,xs,seed=None):
        z=0
        if seed==None:
            seed=random.randint(0,self.user_num)*1000
        LHlist=np.zeros(self.g,int)
        l=0
        for x in xs:
            r.seed(seed+x)
            v=int(r.random()*self.g)  #1-g
            if(LHlist[v]==0):
                LHlist[v]=1
                l+=1
        ur=random.random()
        a=0.0
        for b in range(0,self.g):
            if LHlist[b]==0:
                a+=(1-l*self.p)/(self.g-l)
            if LHlist[b]==1:
                a+=self.p
            if a>ur:
                z=b
                break
        return (z,seed)

    # 调用接口
    def randomizer(self,xs,seed=None):
        z,seed=self.CoreRandomizer(xs,seed)
        return self.recoder(z,seed)

    #解码 ，遍历
    def recoder(self, z, seed):
        pub = np.zeros(self.d, dtype=int)
        for i in range(1, self.d):
            r.seed(seed + i)
            v = int(r.random() * self.g)
            if v == z:
                pub[i] = 1
        return pub
    # 校正
    def decoder(self, hits, n):
        fs = np.array([(hits[i] - n * self.frate) / (self.trate - self.frate) for i in range(0, self.d)])
        return fs

    def MSE(self, Noisy_Vaule_List, True_Value_List, N):
        result = 0
        for i in range(1, len(True_Value_List)):
            tmp = abs(True_Value_List[i] / N - Noisy_Vaule_List[i] / N)
            result += tmp * tmp
        result /= len(True_Value_List)-1
        return result