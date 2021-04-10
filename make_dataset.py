import random

datasets=50#吐き出すデータセット数
min_val=-10**29#乱数の最小値
max_val=10**29#乱数の最大値

path="in\\"#吐き出し先のパス

for d in range(datasets):
    N=random.randint(2,2048)
    A=["{:30f}".format(random.uniform(min_val,max_val))[:30] for i in range(N)]
    A=[i if i[-1]!="." else i.replace(".","") for i in A]
    filename=path+str(d).zfill(4)+".in"
    with open(filename,mode='w') as f:
        f.write("\n".join(A))