import numpy as np
import math
import random
import xxhash
class OLH:
    domain=0
    eps=0.0
    m=0
    usernum=0
    g_first=0.0  #列数
    p_first=0.0 #p
    q_first=0.0 #q
    g_second = 0.0
    p_second = 0.0
    q_second = 0.0

    def __init__(self,D,EPS,USER_NUM,M):
        self.domain=D
        self.eps=EPS
        self.usernum=USER_NUM
        self.m=M
        self.setparams()

    def setparams(self):
        self.g_first=int(round(math.exp(self.eps))) + 1
        self.p_first=math.exp(self.eps) / (math.exp(self.eps) + self.g_first - 1)
        self.q_first=1.0 / (math.exp(self.eps) + self.g_first - 1)
        self.g_second = int(round(math.exp(self.eps/self.m))) + 1
        self.p_second = math.exp(self.eps/self.m) / (math.exp(self.eps/self.m) + self.g_second - 1)
        self.q_second = 1.0 / (math.exp(self.eps/self.m) + self.g_second - 1)

    def OLH_Randomize_First(self,data,seed=None):
        #随机设置种子
        z=0
        if seed==None:
            seed=random.randint(0,self.usernum)
        z = (xxhash.xxh32(data, seed=seed).intdigest() % self.g_first)
        r=np.random.random()
        if r>self.p_first-self.q_first:
           z= np.random.randint(0, self.g_first)
        return z,seed

    def Do_Randomize_First(self,dataset,Noisy_Value_List,seed=None):
        #第一种方法，只取一个
        for itr in dataset:
            tmp = random.randint(0, len(dataset) - 1)
            z,seed=self.OLH_Randomize_First(itr[tmp],seed)
            self.recorder_First(z,seed,Noisy_Value_List)
        #校正
        a = 1.0 * self.g_first / (self.p_first * self.g_first - 1)
        b = 1.0 * self.usernum / (self.p_first * self.g_first - 1)
        for i in range(1,self.domain):
            Noisy_Value_List[i]=(a*Noisy_Value_List[i]-b)*self.m        #乘m

    def recorder_First(self,z,seed,Noisy_Value_List):
        for i in range(1,self.domain):
            if z==(xxhash.xxh32(i,seed=seed).intdigest()%self.g_first):
                Noisy_Value_List[i]+=1


    # 第二种方式。所有都取，epsilon均分
    def OLH_Randomize_Second(self, data, seed=None):
        # 随机设置种子
        z = 0
        if seed == None:
            seed = random.randint(0, self.usernum)
        z = (xxhash.xxh32(data, seed=seed).intdigest() % self.g_second)
        r = np.random.random()
        if r > self.p_second - self.q_second:
            z = np.random.randint(0, self.g_second)
        return z, seed

    def Do_Randomize_Second(self, dataset, Noisy_Value_List, seed=None):
        for itr in dataset:
            for i in itr:
                z, seed = self.OLH_Randomize_Second(i, seed)
                self.recorder_Second(z, seed, Noisy_Value_List)
        # 校正
        a = 1.0 * self.g_second / (self.p_second * self.g_second - 1)
        b = 1.0 * self.usernum / (self.p_second * self.g_second - 1)
        for i in range(1, self.domain):
            Noisy_Value_List[i] = a * Noisy_Value_List[i] - b


    def recorder_Second(self,z,seed,Noisy_Value_List):
        for i in range(1,self.domain):
            if z==(xxhash.xxh32(i,seed=seed).intdigest()%self.g_second):
                Noisy_Value_List[i]+=1

    def MSE(self, Noisy_Vaule_List, True_Value_List, User_num):
        result = 0
        for i in range(1, len(True_Value_List)):
            tmp = abs(True_Value_List[i] / User_num - Noisy_Vaule_List[i] / User_num)
            result += tmp * tmp
        result /= len(True_Value_List) - 1
        return result



