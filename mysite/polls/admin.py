from django.contrib import admin

from .models import Question, Choice

# Register your models here.
# Pollsアプリをadminページ上で編集できるようにする
# admin.site.register(Question)のみだとデフォルトのadminページになるので、変更してみる
# admin.StackInlineだと入力フォームの表示が縦に重なる。TabularInlineだと横に並ぶ
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    #各フィールドの値を表示させるにはlist_displayを設定する
    list_display = ('question_text', 'pub_date', 'was_published_recently')
'''
adminのオプションを変更したいときは、モデルごとにadminクラスを作成して、admin.site.register()の２番目の引数に渡す
'''
admin.site.register(Question, QuestionAdmin)

# Choiceの管理ページを表示する
# admin.site.register(Choice)
# -> Questionモデルを追加するときにChoiceも追加したいので書き換える