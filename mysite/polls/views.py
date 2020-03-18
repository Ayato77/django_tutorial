from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

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
    # Http404の設定(with shortcut)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POSTは辞書のようなオブジェクト。キー指定するとデータにアクセスできる
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question':question, 'error_message':"You didn't select a choice.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # reverseメソッドを使うと、urlのハードコードを防げる
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))