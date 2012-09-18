from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from forms import QuestionForm
from questions.models import Question
from django.conf import settings


def current_question(request):
    form = handle_form(request)
    question = Question.objects.get_current_question()
    params = {
        "question": question,
        "form": form,
        "current": True,
    }
    return render_template(request, "questions/current_question.html", params)


def archive(request):
    form = QuestionForm()
    questions = Question.objects.order_by('-asked_date').filter(asked_date__isnull=False)
    params = {
        "questions": questions,
        "form": form,
    }
    return render_template(request, "questions/archive.html", params)


def detail(request, question_id):
    form = handle_form(request)
    # check if question has been asked
    question = get_object_or_404(Question,
                                 Q(asked_date__isnull=False),
                                 pk=question_id)
    params = {
        "question": question,
        "form": form,
    }
    return render_template(request, "questions/current_question.html", params)


def handle_form(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = Question(question=form.cleaned_data['question'],
                         approved=False)
            q.save()
        else:
            # shouldn't be reached accept if HTML5 validation is bypassed
            print "form not valid"
    else:
        form = QuestionForm()
    return form


def render_template(request, template, params):
    params['twitter_account'] = settings.TWITTER_USER
    return render_to_response(template, params,
                              context_instance=RequestContext(request))
