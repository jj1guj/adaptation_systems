#ソースコード・データセットのフォルダを同階層に配置すること
#g++をたたけるようにしておくこと
"""
|- judge_task1.py
|- ソースコード.c
|- <in> (データセット)
    |- 0000.in
"""
import subprocess
import time
import os
import re

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
    return stdout.decode(), stderr.decode(), rt

if __name__ == "__main__":
    #windowsかUNIXかを取得(実行時に叩くコマンドが変わるため)
    osname=os.name
    #ジャッジするコードのファイル名を入力してもらう
    sourcefile=input("input sourcefile's name: ")

    #テストケースの取得
    testcase_path="in/"
    files=os.listdir(testcase_path)
    testcases=[os.path.join(testcase_path,f) for f in files if os.path.isfile(os.path.join(testcase_path,f))]
    testcases.sort()
    
    #得点を格納しておく
    score_all=[]

    #コンパイル
    #g++にしてるのはWindows系でgccを叩くとウイルスバスターが悪さをしてバイナリを消してしまうことがあるため
    subprocess.run("g++ -o a_task1 -O2 "+sourcefile,shell=True)
    
    #実行コマンドの指定
    if osname=="nt":
        cmd_prefix=".\\a_task1 "
    else:
        cmd_prefix="./a_task1 "

    for i in testcases:
        status=True

        cmd_str=cmd_prefix+i
        start=time.time()
        stdout, stderr, rt = exec_subprocess(cmd_str)
        end=time.time()
        #エスケープシーケンスを削除
        if osname=="nt":
            stdout=stdout[:-2]
        else:
            stdout=stdout[:-1]

        #TLEしていないか
        if end-start>600:
            print(i,"TLE",end-start,"[sec]")
            status=False
            continue

        with open(i,mode="r") as f:
            weight=f.readlines()
        weight=[float(j.replace("\n","")) for j in weight]

        #出力形式が一致しているか確認する
        #print(repr(stdout))
        #print(len(weight),len(stdout))
        if len(weight)!=len(stdout):
            print(i,"WA",end-start,"[sec]")
            status=False
        
        for j in stdout:
            if j!="0" and j!="1":
                print(i,j,"WA",end-start,"[sec]")
                status=False
                break
        
        if status:
            score_all.append(scoring(weight,stdout))
            print(i,score_all[-1],end-start,"[sec]")
        else:
            score_all.append(float('inf'))
        
print("score:",sum(score_all))