#wordpressのファイル構成を調べる
#どんなファイルにアクセス可能か、調べる

import queue		   #リクエストのキューを扱うライブラリ
import threading	   #スレッドを管理するライブラリ
import os		       #OSのファイル階層を取得する
import urllib.request  #URLでの通信を制御
import urllib.error	   #URL通信のエラー制御

#ターゲットのWPのURL
wpurl="http://localhost/blog"

#ローカルのwordpressのディレクトリパス
localwp="/var/www/html/blog"

#スキップ対象の拡張子
filters=[".jpg",".gif",".css"]

#同時に発行するリクエスト数
threads =10

#ローカルのwp
os.chdir(localwp)

#対象URLを格納するための変数
web_paths=queue.Queue()

#ローカルのwpを調査し、ファイル構成
for root,directory,files in os.walk("."):
    for file in files:
        remote_path = "%s/%s"%(root,file)
        if remote_path.startswith("."):
            remote_path=remote_path[1:]
        if os.path.splitext(file)[1] not in filters:
            web_paths.put(remote_path)

#ターゲットのwpを調査する関数
def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url="%s/%s"%(wpurl,path)

        request = urllib.request.Request(url)

        try:
            response=urllib.request.urlopen(request)
            content = response.read()

            print("[%d] => %s"%(response.code,path))
            response.close()

        except urllib.error.HTTPError as error:
            pass

for i in range(threads):
    print("Running thread:%d"%i)
    t=threading.Thread(target=test_remote)
    t.start()
