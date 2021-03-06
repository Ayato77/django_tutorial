import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

'''
djangoオフィシャルが推奨するルール:

モデルやビューごとに TestClass を分割する
テストしたい条件の集まりのそれぞれに対して、異なるテストメソッドを作る
テストメソッドの名前は、その機能を説明するようなものにする

また、さらにテストツールがあるので、そちらも使うことも推奨されている
'''

# Create your tests here.
# was_published_recently()のエラーをテストで検知する

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
                was_published_recently() returns False for questions whose pub_date
                is in the future.
                """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    # create a question with the given 'question_text' and published the given number of days offset to now
    def create_question(question_text, days):
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date = time)

    class QuestionIndexViewTests(TestCase):
        def test_no_questions(self):
            # もし質問がなければ、それに応じたメッセージが表示される
            response = self.client.get(reverse('polls:index'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "No polls are available.")
            self.assertQuerysetEqual(response.context['latest_question_list'], [])

        def test_past_question(self):
            # 過去に作られた質問が表示される
            create_question(question_text = "Past question.", days = -30)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

        def test_future_question(self):
            """
            未来に設定された質問は表示されない
            """
            create_question(question_text="Future question.", days=30)
            response = self.client.get(reverse('polls:index'))
            self.assertContains(response, "No polls are available.")
            self.assertQuerysetEqual(response.context['latest_question_list'], [])

        def test_future_question_and_past_question(self):
            """
            Even if both past and future questions exist, only past questions
            are displayed.過去と未来に設定された質問がそれぞれ両方ある場合、過去の者だけが表示される
            """
            create_question(question_text="Past question.", days=-30)
            create_question(question_text="Future question.", days=30)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(
                response.context['latest_question_list'],
                ['<Question: Past question.>'])

        def test_two_past_questions(self):
            """
            The questions index page may display multiple questions.　indexページが複数の質問を表示できることを試す
            """
            create_question(question_text="Past question 1.", days=-30)
            create_question(question_text="Past question 2.", days=-5)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(
                response.context['latest_question_list'],
                ['<Question: Past question 2.>', '<Question: Past question 1.>']
            )

    class QuestionDetailViewTests(TestCase):
        def test_future_question(self):
            """
            The detail view of a question with a pub_date in the future
            returns a 404 not found. 未来に設定された質問にアクセスすると404が返されることを確認
            """
            future_question = create_question(question_text='Future question.', days=5)
            url = reverse('polls:detail', args=(future_question.id,))
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

        def test_past_question(self):
            """
            The detail view of a question with a pub_date in the past
            displays the question's text.　過去に設定された質問は全て表示できることを確認
            """
            past_question = create_question(question_text='Past Question.', days=-5)
            url = reverse('polls:detail', args=(past_question.id,))
            response = self.client.get(url)
            self.assertContains(response, past_question.question_text)