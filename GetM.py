#获取80%的长度
import numpy as np
from OUE import OUE
class Get_M:
    D=1
    eps=1
    user_num=1
    Noisy_m_length=[]
    True_m_length=[]
    peruser_m=[] #每个用户拥有的数据的数量
    def __init__(self,EPS,USER_NUM):
        self.eps=EPS
        self.user_num=USER_NUM

    # 加载数据
    def load_data_random(self,file_path):
        max=0
        f=open(file_path,"r",encoding="utf-8")
        for line in f.readlines()[:self.user_num]:
            s=line.strip().split(' ')
            if(len(s)>max):
                max=len(s)
        f.close()
        self.D=max+1
        self.Noisy_m_length=np.zeros(self.D,int)
        self.True_m_length = np.zeros(self.D, int)
        f = open(file_path, "r", encoding="utf-8")
        for line in f.readlines()[:self.user_num]:
            s = line.strip().split(' ')
            tmp=len(s)
            self.peruser_m.append([tmp])
            #从1到max
            if tmp>=self.D:
                self.True_m_length[self.D-1]+=1
            else:
                self.True_m_length[tmp]+=1
        f.close()

    # 使用OUE计算长度
    def get_m(self):
        oue=OUE(self.eps,self.D,1)
        oue.Randomize_Mechanism_First(self.peruser_m,self.Noisy_m_length)
        heavy_hitter = 0
        true_heavy = 0
        #测试用，真实的数据，打印真正80%的长度
        for i in range(1,self.D):
            true_heavy+=self.True_m_length[i]
            if(true_heavy>=0.8*self.user_num):
                print(i)
                break

        #扰动后的80%
        for i in range(1,self.D):
            if(self.Noisy_m_length[i]<0):
                continue
            heavy_hitter+=self.Noisy_m_length[i]
            if heavy_hitter>=0.8*self.user_num:
                print(i)
                return i
