from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from .models import Question

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
    # 最新５つの質問をレスポンスする
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # コンテキストはテンプレート変数名をPythonオブジェクトにマッピングする辞書
    context = {'latest_question_list':latest_question_list}
    # renderをつかうとテンプレートのロードをわざわざしなくてもいい
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # Http404の設定(without short cut)
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)