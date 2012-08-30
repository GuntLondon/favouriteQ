from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import QuestionForm
from questions.models import Question, Answer

def current_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = Question(question=form.cleaned_data['question'], approved=False)
            q.save()
        else:
            print "form not valid"

    question = Question.objects.get_current_question()
    return render_to_response('questions/current_question.html', {"question": question}, context_instance=RequestContext(request))