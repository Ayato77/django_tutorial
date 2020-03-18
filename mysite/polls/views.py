from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

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


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

# DetailView 汎用ビューには、 "pk" という名前で
# URL からプライマリキーをキャプチャして渡すことになっているので、
# 汎用ビュー向けに question_id を pk に変更しています。
class DetailView(generic.DetailView):
    #  各汎用ビューは自分がどのモデルに対して動作するのか知っておく必要があるのでmodel=を設定しておく。
    model = Question
    # template_name属性の指定をすると、デフォルトではなく、指定したテンプレート名を使うように指定できる。
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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