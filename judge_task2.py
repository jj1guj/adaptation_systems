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
import sys
import subprocess
import time
import os

def scoring(weight,Ans):
    Sum=[0,0]
    for i in range(len(weight)):
        Sum[int(Ans[i])]+=weight[i]
    return abs(Sum[0]-Sum[1])

def exec_subprocess(cmd: str) -> (str, str, int):
    """
    OSコマンドを実行し結果を返す
    :param cmd: コマンド文字列
    :return: 標準出力、標準エラー出力、リターンコードのタプル
    """
    child = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = child.communicate()
    rt = child.returncode
    return stdout.decode(), stderr.decode(),rt
    #return stdout.decode(), stderr.decode(), rt

if __name__ == "__main__":
    #引数の設定
    parser=argparse.ArgumentParser(description="judge task 1")
    parser.add_argument("--path","-p",type=str,default="in",help="testcases' path")
    parser.add_argument("--source","-s",type=str,help="sourcefile to judge",required=True)
    parser.add_argument("--split_mode","-m",nargs='*',default="r",
    help="specify split mode. r: random, f [filename]: use file, n [number]: all testcases will be splited [number]")
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

    #分割数の指定
    if args.split_mode[0]=="r":
        split_num=[random.randint(2,16) for i in range(len(testcases))]
    elif args.split_mode[0]=="f":
        if len(args.split_mode)==2 and os.path.exists(args.split_mode[1]):
            with open(args.split_mode[1],mode="r") as f:
                split_num=f.readlines()
            split_num=[int(i.replace("\n","")) for i in split_num]
        else:
            sys.exit()
    elif args.split_mode[0]=="n" and len(args.split_mode)==2 and args.split_mode[1].isdecimal():
        if int(args.split_mode[1])>=2 and int(args.split_mode[1])<=16:
            split_num=[int(args.split_mode[1]) for i in range(len(testcases))]
        else:
            sys.exit()
    else:
        sys.exit()

    #得点を格納しておく
    score_all=[]

    #コンパイル
    #g++にしてるのはWindows系でgccを叩くとウイルスバスターが悪さをしてバイナリを消してしまうことがあるため
    subprocess.run("g++ -o a_task1 -O3 "+sourcefile,shell=True)
    
    #実行コマンドの指定
    if osname=="nt":
        cmd_prefix=".\\a_task1 "
    else:
        cmd_prefix="./a_task1 "

    for case in range(len(testcases)):
        i=testcases[case]
        status=True

        cmd_str=cmd_prefix+" "+str(split_num[case])+" "+i
        start=time.time()
        stdout, stderr, rt = exec_subprocess(cmd_str)
        end=time.time()
        L=stdout.split("\n")
        for j in L:
            if  j!="" and j[0]!="#":
                stdout=j
        #エスケープシーケンスを削除
        if osname=="nt":
            #あとで検証する
            L=stdout.split("\r")
            stdout=L[0]
        """
        else:
            stdout=stdout[:-1]
        """

        #TLEしていないか
        if end-start>600:
            print(i,"TLE",end-start,"[sec]")
            status=False
            continue

        with open(i,mode="r") as f:
            weight=f.readlines()
        weight=[float(j.replace("\n","")) for j in weight]

        #出力形式が一致しているか確認する
        if len(weight)!=len(stdout):
            print(i,"WA",end-start,"[sec]")
            status=False
        
        dic={"A":10,"B":11,"C":12,"D":13,"E":14,"F":15}
        for j in stdout:
            if j in dic:
                num=dic[j]
            elif not j.isdecimal():
                status=False
                break
            else:
                num=int(j)

            if num<0 and num>=split_num[case]:
                print(i,j,"WA",end-start,"[sec]")
                status=False
                break
        
        if status:
            score_all.append(scoring(weight,stdout))
            print(i,score_all[-1],end-start,"[sec]")
        else:
            score_all.append(float('inf'))
        
    print("score:",sum(score_all))