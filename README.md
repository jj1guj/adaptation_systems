<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
<script type="text/x-mathjax-config">
 MathJax.Hub.Config({
 tex2jax: {
 inlineMath: [['$', '$'] ],
 displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
 }
 });
</script>

# adaptation_systems
適応システム構成論(0AL5524)での課題を快適に行うためのスクリプトたち
# 動作環境
・Python3(Python3.7及びPython3.8での正常な動作を確認しています)  
・ターミナルもしくはコマンドプロンプトから`g++`がたたけること(Windowsでたたけない場合はMinGWをインストールしてください)
# 使い方
## テストケースの生成
```
python make_dataset.py
```
デフォルトではテストケースが50個生成されるようになっています.  
生成するテストケースの数を変えたい場合は`make_dataset.py`内の`datasets`の値を変えてください.  
テストケースは`in`というディレクトリ内にすべて吐き出されます(ディレクトリが生成されていない場合は自動で生成します)

## 課題1のジャッジ
`judge_task1.py`, 作成したソースコード, 生成したテストケースのディレクトリ(`in`)をすべて同じ階層に入れるようにして下さい.  
```
python judge_task1.py
```
これを叩くと作成したソースコードのファイル名の入力が求められるので入力し, 実行してください.  
スコアの算出は各テストケースでのグループ0とグループ1の差の絶対とを取り, すべて足しています.  
そのため, 最終的に出てきたスコアが低ければ低いほどいいです.