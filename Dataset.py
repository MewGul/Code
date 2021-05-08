#加载数据
import random
class DataSet:
    def __init__(self):
        self.records=[]

    #随机长度数据
    def create_data_random(self,file_path,startlocation):
        f=open(file_path,"r",encoding="utf-8")
        for line in f.readlines()[startlocation:]:
            s=line.strip().split(' ')
            s=[int(x)for x in s]
            tmp=s
            self.records.append(tmp)

    #固定长度数据
    def create_data_certain(self,file_path,length,startlocation,D,data_map):
        f=open(file_path,"r",encoding="utf-8")
        for line in f.readlines()[startlocation:]:
            s=line.strip().split(' ')
            s = [int(x) for x in s]
            if len(s)<length:
                s_length=len(s)
                for i in range(0,length-s_length):
                    s.append(D+i)
                    if data_map.get(D+i)==None:
                        data_map.update({D+i:len(data_map)+1})
                self.records.append(s)
            else:
                tmp=random.sample(s,length)
                self.records.append(tmp)

    #上限长度,不够不填充
    def create_data_unfilled(self,file_path,length,startlocation):
        f = open(file_path, "r", encoding="utf-8")
        for line in f.readlines()[startlocation:]:
            s = line.strip().split(' ')
            s = [int(x) for x in s]
            tmp = []
            if(len(s)>length):
                tmp=random.sample(s,length)
            else:
                tmp = s
            self.records.append(tmp)
    #最大值
    def max_valued(self):
        max=0
        for i in self.records:
            for j in i:
                if j>max:
                    max=j
        return max

    #将数据编号，数据转化为map
    def transform_to_map(self,data_map):
        num=1
        for i in self.records:
            for j in i:
                if data_map.get(j)==None:
                    data_map.update({j:num})
                    num+=1

    #将数据转化为编号
    def transform_to_numbered_data(self,data_map,data_list):
        num=len(data_map)
        for i in self.records:
            tmp = []
            for j in i:
                if data_map.get(j)==None:
                    data_map.update({j:num})
                tmp.append(data_map[j])
            data_list.append(tmp)









