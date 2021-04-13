#ソースコード・データセットのフォルダを同階層に配置すること
#g++をたたけるようにしておくこと
"""
|- judge_task1.py
|- ソースコード.c
|- <in> (データセット)
    |- 0000.in
"""
import argparse
import subprocess
import time
import os

def scoring(weight,Ans):
    Sum=[0,0]
    for i in range(len(weight)):
        Sum[int(Ans[i])]+=weight[i]
    return abs(Sum[0]-Sum[1])

if __name__ == "__main__":
    #引数の設定
    parser=argparse.ArgumentParser(description="judge task 1")
    parser.add_argument("--path","-p",type=str,default="in",help="testcases' path")
    parser.add_argument("--source","-s",type=str,help="sourcefile to judge",required=True)
    args=parser.parse_args()

    #windowsかUNIXかを取得(実行時に叩くコマンドが変わるため)
    osname=os.name
    #ジャッジするコードのファイル名を入力してもらう
    sourcefile=args.source

    #テストケースの取得
    testcase_path=args.path
    files=os.listdir(testcase_path)
    testcases=[os.path.join(testcase_path,f) for f in files if os.path.isfile(os.path.join(testcase_path,f))]
    testcases.sort()

    #コンパイル
    #g++にしてるのはWindows系でgccを叩くとウイルスバスターが悪さをしてバイナリを消してしまうことがあるため
    subprocess.run("g++ -o a_task1 -O3 "+sourcefile,shell=True)
    
    #実行コマンドの指定
    if osname=="nt":
        cmd_prefix=".\\a_task1 "
    else:
        cmd_prefix="./a_task1 "

    #並列で実行して解を得る
    procs=[]
    for i in testcases:
        cmd_str=cmd_prefix+i
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
        
        for j in stdout:
            if j!="0" and j!="1":
                print(i,j,"WA")
                status=False
                break
        
        if status:
            score_all.append(scoring(weight,stdout))
            print(i,score_all[-1])
        else:
            score_all.append(float('inf'))

    print("score:",sum(score_all))