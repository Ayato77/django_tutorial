from django.db import models

# Create 2 models:
# 1. Poll with 2 columns question and publication date
# 2. Choice with 2 columns choice_text and vote
# Any choice has relationship with an question
# djangoのモデルとは、データのテーブル作成のようなもの。クラスが表の名前でその中にカテゴリを記述するイメージ

class Question(models.Model):
    question_text = models.CharField(max_length=200)# CharFieldは引数としてmax_legth()が必須
    pub_date = models.DateTimeField('date published')# pub_dateでは人間に読めないので、新たにデータ名としてdate publishedを設定

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)# それぞれのChoiceが一つのQuestionに関連している
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)