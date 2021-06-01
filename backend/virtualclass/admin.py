from django.contrib import admin
from .models import Student, Video, Quiz, Question, Answer
from django.db.models import Q


class QuizInfoInline(admin.TabularInline):
    model = Student.quiz_info.through


class QuizAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['id', 'title']
    inlines = [
        QuizInfoInline,
    ]


class AnswerInline(admin.TabularInline):
    model = Answer


class QuizQuestionFilter(admin.SimpleListFilter):
    title = 'quiz'
    parameter_name = 'quiz'

    def lookups(self, request, model_admin):  # create clickable links on right hand side
        quizzes = Quiz.objects.all()
        lookups = ()
        for quiz in quizzes:
            lookups += ((quiz.title, quiz.title),)
        return lookups

    def queryset(self, request, queryset):  # return all the ojbects that fit the parameter set
        if self.value():  # why is self.value() containing the year?
            quiz_title = self.value()
            return queryset.filter(Q(quiz__title=quiz_title))


class QuestionAdmin(admin.ModelAdmin):
    fields = [
        'prompt',
        'quiz',
    ]
    list_display = ['id', 'prompt', 'quiz']
    list_filter = [QuizQuestionFilter, ]
    search_fields = ['quiz', 'title']
    inlines = [AnswerInline, ]


class AnswerQuestionFilter(admin.SimpleListFilter):
    title = 'quiz'
    parameter_name = 'quiz'

    def lookups(self, request, model_admin):  # create clickable links on right hand side
        quizzes = Quiz.objects.all()
        lookups = ()
        for quiz in quizzes:
            lookups += ((quiz.title, quiz.title),)
        return lookups

    def queryset(self, request, queryset):  # return all the ojbects that fit the parameter set
        if self.value():  # why is self.value() containing the year?
            quiz_title = self.value()
            return queryset.filter(Q(question__quiz__title=quiz_title))


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'correct', 'question']
    list_filter = [AnswerQuestionFilter, ]


class StudentAdmin(admin.ModelAdmin):
    inlines = [
        QuizInfoInline,
    ]


# admin.site.register(Student, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Video)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
