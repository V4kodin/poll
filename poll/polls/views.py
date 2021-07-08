from typing import List

from rest_framework.views import APIView, Response, Request
from rest_framework import status
from django.shortcuts import get_list_or_404
from drf_yasg.utils import swagger_auto_schema

from .models import Quiz, Question, AnswerTracker
from .serializer import (
    QuizSerializer,
    QuestionSerializer,
    AnswerSerializer,
    AnswerTrackerSerializer
)
from .yasg import report_params, report_response, answer_request_body

# Список опросов
class QuizzesListView(APIView):

    # Возврат списка всех актуальных опросов
    @swagger_auto_schema(responses={200: QuizSerializer(many=True)})
    def get(self, request: Request) -> Response:
        active_quizzes_qs = Quiz.get_active()
        serialized_data = QuizSerializer(active_quizzes_qs, many=True)
        return Response(serialized_data.data)

# Просмотр вопросов определенного опроса
class QuizDetailView(APIView):

    # Возврат всех вопросов опроса
    @swagger_auto_schema(responses={200: QuestionSerializer(many=True)})
    def get(self, request: Request, quiz_id: int) -> Response:

        quiz_qs = get_list_or_404(Question, quiz_id=quiz_id)
        serialized_data = QuestionSerializer(quiz_qs, many=True)
        return Response(serialized_data.data)

# Сбор ответов пользователей
class AnswerTrakerView(APIView):

    # Сохраняет ответы пользователей
    @swagger_auto_schema(request_body=answer_request_body)
    def post(self, request: Request, quiz_id: int) -> Response:
        parsed_answers: List[dict] = self.parse_request(request, quiz_id)
        serialized_answers = AnswerTrackerSerializer(data=parsed_answers, many=True)
        if serialized_answers.is_valid(raise_exception=True):
            serialized_answers.save()
            return Response(serialized_answers.data, status=status.HTTP_201_CREATED)
        return Response(serialized_answers.errors, status=status.HTTP_400_BAD_REQUEST)

    # Парсинг ответов
    def parse_request(self, request: Request, quiz_id: int) -> List[dict]:

        parsed_answers: List[dict] = []
        for question in request.data['answers']:
            answer: dict = {}
            answer['quiz_id'] = quiz_id
            answer['customer'] = request.data['customer']
            answer['question_id'] = question['id']
            answer['answer_text'] = question.get('answer_text', '')
            if question.get('choices'):
                for choice in question['choices']:
                    answer['choice_id'] = choice
                    parsed_answers.append(answer.copy())
            else:
                parsed_answers.append(answer.copy())
        return parsed_answers

# Отчет об ответах пользователей
class ReportView(APIView):

    @swagger_auto_schema(
        responses=report_response,
        manual_parameters=report_params,
    )
    # Получить отчет с ответами клиентов
    def get(self, request: Request) -> Response:

        customer: str = request.query_params.get('customer')
        report = get_list_or_404(AnswerTracker, customer=customer)
        serialized_report = AnswerSerializer(report, many=True)
        parsed_report = self.parse_report(serialized_report.data)
        return Response(parsed_report)

    # Парсинг сериализованные данные до необходимой структуры
    def parse_report(self, serialized_report: List[dict]) -> List[dict]:

        quizzes: set = set(answer['quiz'] for answer in serialized_report)
        parsed_report: dict = {quiz: [] for quiz in quizzes}
        for answer in serialized_report:
            parsed_report[answer.pop('quiz')].append(answer)
        return parsed_report
