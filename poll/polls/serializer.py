from rest_framework import serializers

from .models import Quiz, Question, AnswerTracker, Choice

# Сериалайзер опросов
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

# Выбор сериализатора модели
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text']

# Сериализатор модели вопроса
class QuestionSerializer(serializers.ModelSerializer):
    choice_set = ChoiceSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'choice_set']

# Сериализатор модели AnswerTracker
class AnswerTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerTracker
        fields = '__all__'

# Сериализатор для представления отчета
class AnswerSerializer(serializers.Serializer):
    quiz = serializers.SerializerMethodField('get_quiz_title')
    question = serializers.SerializerMethodField('get_question_text')
    answer_text = serializers.CharField()
    choice = serializers.SerializerMethodField('get_choice_text')

    def get_quiz_title(self, obj):
        return obj.quiz_id.title

    def get_question_text(self, obj):
        return obj.question_id.question_text

    def get_choice_text(self, obj):
        return obj.choice_id.choice_text if obj.choice_id else None

# Сериализатор модели AnswerTracker с ограниченными полями
class AnsweredQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerTracker
        fields = ['question_id', 'choice_id', 'answer_text']