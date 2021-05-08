import numpy as np
from Dataset import DataSet
from OUE import OUE
from GetM import Get_M
from WHEEL import Wheel
from Disperse_WHEEL import Disperse_Wheel
from OLH import OLH
#封装的函数获取epsilon
EPS=1
M=1 #每个用户的数据多少
getm_usernum=30000#获取80%的m使用的用户数量
D=1 #domain

#获取80%用户的长度
get_m=Get_M(EPS,getm_usernum)
get_m.load_data_random('kosarak.dat')
M=get_m.get_m()
#####################

#获取全部的数据
Data1=DataSet()
Data1.create_data_random('kosarak.dat',0)
max_num=Data1.max_valued()
#D=max_num+1


#数据集进行编号,用map存储
map_data={}
Data1.transform_to_map(map_data)
map_length=len(map_data)
D=map_length+1
#####################

#数据等长处理,对不够长的进行填充，更新map_data表
Data2=DataSet()
Data2.create_data_certain('kosarak.dat',M,getm_usernum,D,map_data)
numbered_data=[]#这里将其转化为编完号的表，可以直接使用这个
Data2.transform_to_numbered_data(map_data,numbered_data)
user_num=len(numbered_data)
#存储真实数据和扰动后数据，下标从1到max_num，总长度length为max_num+1
True_Value_List=np.zeros(D,int)
Noisy_Value_List_OUE_First=np.zeros(D,int)
Noisy_Value_List_OUE_Second=np.zeros(D,int)
Noisy_Value_List_WHEEL=np.zeros(D,int)
Noisy_Value_List_Disperse_WHEEL=np.zeros(D,int)
Noisy_Value_List_OLH_First=np.zeros(D,int)
Noisy_Value_List_OLH_Second=np.zeros(D,int)
for itr in numbered_data:
    for i in itr:
        if i >=D:
            continue
        else:
            True_Value_List[i]+=1


#测试区
Data3=DataSet()
Data3.create_data_unfilled('kosarak.dat',M,getm_usernum,)
test_numbered_data=[]#这里将其转化为编完号的表，可以直接使用这个
Data3.transform_to_numbered_data(map_data,test_numbered_data)
test_user_length=len(test_numbered_data)
test_disperse_wheel=Disperse_Wheel(EPS,D,M,test_user_length)
hit=np.zeros(D,dtype=int)
for index,itr in enumerate(test_numbered_data):
    pub=test_disperse_wheel.randomizer(itr)
    hit=np.array(hit)+np.array(pub)
fs=test_disperse_wheel.decoder(hit,test_user_length)
for index, value in enumerate(Noisy_Value_List_Disperse_WHEEL):
    Noisy_Value_List_Disperse_WHEEL[index] = fs[index]
mse=test_disperse_wheel.MSE(Noisy_Value_List_Disperse_WHEEL,True_Value_List,test_user_length)
print("Disperse_WHEEL:", mse)




######################





#OUE方法
oue=OUE(EPS,D,M)
#随机取一个的方法
oue.Randomize_Mechanism_First(numbered_data,Noisy_Value_List_OUE_First)
#并行定律，都取，分epsilon的方法
oue.Randomize_Mechanism_Second(numbered_data,Noisy_Value_List_OUE_Second)

#wheel方法
wheel=Wheel(D,M,EPS,len(numbered_data))
hits=np.zeros(D,dtype=int)
for index,itr in enumerate(numbered_data):
    pub=wheel.randomizer(itr)
    hits=np.array(hits)+np.array(pub)
fs=wheel.decoder(hits,user_num)
for index, value in enumerate(Noisy_Value_List_WHEEL):
    Noisy_Value_List_WHEEL[index] = fs[index]


#枚举型wheel
disperse_wheel=Disperse_Wheel(EPS,D,M,user_num)
hit=np.zeros(D,dtype=int)
for index,itr in enumerate(numbered_data):
    pub=disperse_wheel.randomizer(itr)
    hit=np.array(hit)+np.array(pub)
fs=disperse_wheel.decoder(hit,len(numbered_data))
for index, value in enumerate(Noisy_Value_List_Disperse_WHEEL):
    Noisy_Value_List_Disperse_WHEEL[index] = fs[index]

#OLH
olh=OLH(D,EPS,user_num,M)
#随机取一个扰动
olh.Do_Randomize_First(numbered_data,Noisy_Value_List_OLH_First)
#每个都扰动
olh.Do_Randomize_Second(numbered_data,Noisy_Value_List_OLH_Second)