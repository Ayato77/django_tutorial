from django.shortcuts import render

from django.http import HttpResponse

'''
簡単なビュー作成。ビューを呼び出すためにはURLを対応づける必要がある -> URLconf
アプリケーションのディレクトリにurls.pyを作成して、URLconfを作る。

投票アプリケーションでは、以下4つのビューを作成します:

- 質問 "インデックス" ページ -- 最新の質問をいくつか表示
- 質問 "詳細" ページ -- 結果を表示せず、質問テキストと投票フォームを表示
- 質問 "結果" ページ -- 特定の質問の結果を表示
- 投票ページ -- 特定の質問の選択を投票として受付
'''


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)