del_name=set() # 剔除的队伍列表, 从cut.csv中读入，星号*属于非法字符会导致滚榜BUG，含*队伍必须剔除
dict_name={} # nickname to realname 的数据，数据从change.csv中读入，可只提供部分

with open("cut.csv","r") as f:
    for line in f:
        tmp=line.rstrip("\n")
        del_name.add(tmp)

with open("change.csv","r") as f:
    for line in f:
        tmp=line.rstrip("\n").split(",")
        dict_name[tmp[0]]=tmp[1]

# print(del_name)
# print(dict_name)

import json
data=json.load(open("data/data.json", encoding="utf-8"))

ans=data.copy()
ans["data"]=[]
for i in data["data"]:
    s=i["username"]
    if s not in del_name:
        if s in dict_name: i["username"]=dict_name[s]
        ans["data"].append(i)

json.dump(ans, open("data/data.json", "w", encoding="utf-8"), indent=4)

