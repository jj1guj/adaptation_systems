#ソースコード・データセットのフォルダを同階層に配置すること
#g++をたたけるようにしておくこと
"""
|- judge_task1.py
|- ソースコード.c
|- <in> (データセット)
    |- 0000.in
"""
import argparse
import random
import subprocess
import sys
import time
import os

def scoring(weight,split_num,Ans):
    Sum=[0 for i in range(split_num)]
    for i in range(len(weight)):
        Sum[int(Ans[i])]+=weight[i]
    return max(Sum)-min(Sum)

if __name__ == "__main__":
    #引数の設定
    parser=argparse.ArgumentParser(description="judge task 2")
    parser.add_argument("--path","-p",type=str,default="in",help="testcases' path")
    parser.add_argument("--source","-s",type=str,help="sourcefile to judge",required=True)
    parser.add_argument("--split_mode","-m",nargs='*',default="r",
    help="specify split mode. r: random, f [filename]: use file, n [number]: all testcases will be splited [number]")
    args=parser.parse_args()

    #windowsかUNIXかを取得(実行時に叩くコマンドが変わるため)
    osname=os.name
    #ジャッジするコードのファイル名を入力してもらう
    sourcefile=args.source
    if not os.path.exists(sourcefile):
        sys.exit()

    #テストケースの取得
    testcase_path=args.path
    files=os.listdir(testcase_path)
    testcases=[os.path.join(testcase_path,f) for f in files if os.path.isfile(os.path.join(testcase_path,f))]
    testcases.sort()

    #分割数の指定
    if args.split_mode[0]=="r":
        split_num=[random.randint(2,16) for i in range(len(testcases))]
    elif args.split_mode[0]=="f":
        if len(args.split_mode)==2 and os.path.exists(args.split_mode[1]):
            with open(args.split_mode[1],mode="r") as f:
                split_num=f.readlines()
            split_num=[int(i.replace("\n","")) for i in split_num]
            l=[i for i in split_num if i<2 and i>16]
            if len(split_num)<len(testcases) or len(l)>0:
                sys.exit()
        elif not os.path.exists(args.split_mode[1]):
            #なかったらランダムに作る
            split_num=[random.randint(2,16) for i in range(len(testcases))]
            with open(args.split_mode[1],mode="w") as f:
                f.write("\n".join(map(str,split_num)))
        else:
            sys.exit()
    elif args.split_mode[0]=="n" and len(args.split_mode)==2 and args.split_mode[1].isdecimal():
        if int(args.split_mode[1])>=2 and int(args.split_mode[1])<=16:
            split_num=[int(args.split_mode[1]) for i in range(len(testcases))]
        else:
            sys.exit()
    else:
        sys.exit()

    #コンパイル
    #g++にしてるのはWindows系でgccを叩くとウイルスバスターが悪さをしてバイナリを消してしまうことがあるため
    subprocess.run("g++ -o a_task2 -O3 "+sourcefile,shell=True)
    
    #実行コマンドの指定
    if osname=="nt":
        cmd_prefix=".\\a_task2 "
    else:
        cmd_prefix="./a_task2 "

    #並列で実行して解を得る
    procs=[]
    for case in range(len(testcases)):
        i=testcases[case]
        cmd_str=cmd_prefix+" "+str(split_num[case])+" "+i
        procs.append(subprocess.Popen(cmd_str,shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    Ans=[0 for i in range(len(testcases))]
    for i in range(len(procs)):
        stdout,stderr=procs[i].communicate()
        stdout=stdout.decode()
        L=stdout.split("\n")
        for j in L:
            if j!="" and j[0]!="#":
                stdout=j
        Ans[i]=stdout
    Ans=[i.split("\r")[0] if osname=='nt' else i for i in Ans]

    #得点を格納しておく
    score_all=[]
    for k in range(len(testcases)):
        status=True
        i=testcases[k]
        stdout=Ans[k]
        with open(i,mode="r") as f:
            weight=f.readlines()
        weight=[float(j.replace("\n","")) for j in weight]

        #出力形式が一致しているか確認する
        if len(weight)!=len(stdout):
            print(i,"WA")
            status=False
        
        dic={"A":10,"B":11,"C":12,"D":13,"E":14,"F":15}
        Ans_i=[]
        for j in stdout:
            if j in dic:
                num=dic[j]
            elif not j.isdecimal():
                print(i,j,"WA")
                status=False
                break
            else:
                num=int(j)
            
            if num<0 and num>=split_num[case]:
                print(i,j,"WA")
                status=False
                break
            Ans_i.append(num)
        
        if status:
            score_all.append(scoring(weight,split_num[k],Ans_i))
            print(i,score_all[-1])
        else:
            score_all.append(float('inf'))

    print("score:",sum(score_all))