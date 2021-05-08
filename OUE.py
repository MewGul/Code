import numpy as np
import math
import random
E=math.e
class OUE:
    p=0.0
    q_first=0.0
    q_second=0.0
    eps=0.0
    m=1
    domain=1
    def __init__(self,eps,dom,M):
        self.eps=eps
        self.domain=dom
        self.m=M
        self.p=0.5
        self.q_first=1/float(1+E**eps)
        self.q_second=1/float(1+E**(self.eps/self.m))
    def OUE_Query_First(self,value):
        result=0
        if(value==1):
            if(np.random.random()<self.p):
                result=1
        else:
            if(np.random.random()<self.q_first):
                result=1
        return result
    def OUE_Randomize_First(self,data,Noisy_Value_List):
        for itr in range(1,len((Noisy_Value_List))):
            if(int(data)!=itr):
                Noisy_Value_List[itr]+=self.OUE_Query_First(0)
            if(int(data)==itr):
                Noisy_Value_List[itr]+=self.OUE_Query_First(1)
    def Randomize_Mechanism_First(self,dataset,Noisy_Value_List):
        #第一种方法，只取一个
        for itr in dataset:
            tmp=random.randint(0,len(itr)-1)
            self.OUE_Randomize_First(itr[tmp],Noisy_Value_List)
        #校正
        for i in range(1,len(Noisy_Value_List)):
            Noisy_Value_List[i] = self.m*(Noisy_Value_List[i] - len(dataset) * self.q_first) / (self.p - self.q_first)
            if Noisy_Value_List[i]<0:
                Noisy_Value_List[i]=0

    # 第二种方案
    def OUE_Query_Second(self,value):
        result=0
        if (value == 1):
            if (np.random.random() < self.p):
                result = 1
        else:
            if (np.random.random() < self.q_first):
                result = 1
        return result
    def OUE_Randomize_Second(self,data,Noisy_Value_List):
        for itr in range(1, len((Noisy_Value_List))):
            if (int(data) != itr):
                Noisy_Value_List[itr] += self.OUE_Query_Second(0)
            if (int(data) == itr):
                Noisy_Value_List[itr] += self.OUE_Query_Second(1)
    def Randomize_Mechanism_Second(self,dataset,Noisy_Value_List):
        #第二种方法，m全都取，隐私预算分一分epsilon/m
        for itr in dataset:
            for i in itr:
                self.OUE_Randomize_Second(i,Noisy_Value_List)
        #校正，用第二种的p,q校正
        for i in range(1,len(Noisy_Value_List)):
            Noisy_Value_List[i] = (Noisy_Value_List[i] - len(dataset) * self.q_second) / (self.p - self.q_second)
            if Noisy_Value_List[i]<0:
                Noisy_Value_List[i]=0

    def MSE(self, Noisy_Vaule_List, True_Value_List, User_num):
        result = 0
        for i in range(1, len(True_Value_List)):
            tmp = abs(True_Value_List[i] / User_num - Noisy_Vaule_List[i] / User_num)
            result += tmp * tmp
        result /= len(True_Value_List) - 1
        return result