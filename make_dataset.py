import argparse
import random
import os

#引数の設定
parser=argparse.ArgumentParser(description="make testcases")
parser.add_argument("--path","-p",type=str,default="in",help="testcases' path")
parser.add_argument("--testcase_num","-t",type=int,default=50,help="number of testcases")
parser.add_argument("--data_min","-dmin",type=int,default=2,help="minimum number of each testcases")
parser.add_argument("--data_max","-dmax",type=int,default=2048,help="minimum number of each testcases")
parser.add_argument("--min","-min",type=float,default=0,help="minimun value of each testcases")
parser.add_argument("--max","-max",type=float,default=1,help="maximun value of each testcases")
parser.add_argument("--seed","-s",type=int,default=0,help="random number's seed")
args=parser.parse_args()

random.seed(args.seed)
datasets=args.testcase_num#吐き出すデータセット数
min_val=min(args.min,args.max)#乱数の最小値
max_val=max(args.min,args.max)#乱数の最大値

path=args.path#吐き出し先のパス

#ディレクトリが存在しなかったら作成
if not os.path.isdir(path):
    os.makedirs(path)

def reduce_digit(s):
    for i in reversed(range(len(s))):
        if s[i] == '0':
            s = s[:i]
        else:
            break
    if s[-1]==".":
        s=s[:-1]
    return s

for d in range(datasets):
    N=random.randint(min(args.data_min,args.data_max),max(args.data_min,args.data_max))
    #30桁の乱数を生成
    A=[]
    for i in range(N):
        #整数部を生成(min<=x<=max)
        x=random.randint(args.min,args.max)
        xdigits=len(str(x))
        if x<0:
            xdigits-=1
        if x==args.max:
            A.append(str(x)+"."+''.join("0" for _ in range(30-xdigits)))
        else:
            A.append(str(x)+"."+''.join(str(random.randint(0, 9)) for _ in range(30-xdigits)))
    A=[reduce_digit(i) for i in A]
    filename=os.path.join(path,str(d+args.seed).zfill(4)+".in")
    with open(filename,mode='w') as f:
        f.write("\n".join(A))
