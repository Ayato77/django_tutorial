import datetime

from django.db import models
from django.utils import timezone

# Create 2 models:
# 1. Poll with 2 columns question and publication date
# 2. Choice with 2 columns choice_text and vote
# Any choice has relationship with an question
# djangoのモデルとは、データのテーブル作成のようなもの。クラスが表の名前でその中にカテゴリを記述するイメージ

# モデル変更の３ステップ
# 1. モデルを変更する (models.py の中の)
# 2. これらの変更のためのマイグレーションを作成するために python manage.py makemigrations を実行します。
# 3. データベースにこれらの変更を適用するために python manage.py migrate を実行します。

# 各モデルに__str()__メソッドを追加するように心がけること！！

class Question(models.Model):
    question_text = models.CharField(max_length=200)# CharFieldは引数としてmax_legth()が必須
    pub_date = models.DateTimeField('date published')# pub_dateでは人間に読めないので、新たにデータ名としてdate publishedを設定
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)# それぞれのchoiceが一つのquestionと関連づけられている
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text