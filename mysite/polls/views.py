from django.shortcuts import render

from django.http import HttpResponse

# 簡単なビュー作成。ビューを呼び出すためにはURLを対応づける必要がある -> URLconf
# アプリケーションのディレクトリにurls.pyを作成して、URLconfを作る。

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
