import random
import os

datasets=50#吐き出すデータセット数
min_val=-1#乱数の最小値
max_val=1#乱数の最大値

path="in"#吐き出し先のパス

#ディレクトリが存在しなかったら作成
if not os.path.isdir(path):
    os.makedirs(path)

for d in range(datasets):
    N=random.randint(2,2048)
    A=[str(random.uniform(min_val,max_val)) for i in range(N)]
    A=[i if i[-1]!="." else i.replace(".","") for i in A]
    filename=os.path.join(path,str(d).zfill(4)+".in")
    with open(filename,mode='w') as f:
        f.write("\n".join(A))