# Generated by Django 2.2.10 on 2021-07-08 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizzes',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=1000)),
                ('question_type', models.CharField(choices=[('radio', 'radio'), ('checkbox', 'checkbox'), ('text', 'text')], default='radio', max_length=8)),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Quiz')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=1000)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question')),
            ],
            options={
                'verbose_name': 'Choice',
                'verbose_name_plural': 'Choices',
            },
        ),
        migrations.CreateModel(
            name='AnswerTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.IntegerField(verbose_name='customer_id')),
                ('answer_text', models.TextField()),
                ('choice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Choice')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question')),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Quiz')),
            ],
            options={
                'verbose_name': 'Answer Tracker',
                'verbose_name_plural': 'Answers Tracker',
            },
        ),
    ]
