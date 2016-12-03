from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotModified
from django.views.decorators.http import require_GET, require_POST
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from qa.models import Answer
from qa.models import Question
from qa.models import Profile
from qa.models import Tag
from qa.forms import AskForm, AnswerForm, SignUpForm


# Create your views here.
from django.http import HttpResponse


def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 5))
    except ValueError:
        limit = 5
    if limit > 100:
        limit = 5

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    paginator = Paginator(qs, limit)

    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page, paginator


def get_right_column():
    return Profile.objects.top(), Tag.objects.top()


def mixin(dic, **kwargs):
    top_members, top_tags = get_right_column()
    # top_tags.baseurl = reverse('tag_question')
    top_tags.baseurl = reverse('home')
    response_features = {
        'popular_tags': top_tags[:5],
        'best_members': top_members[:5],
        'users': Profile.objects.all()
    }
    response_features.update(dic)
    return response_features


def index(request):
    questions = Question.objects.new()
    page, paginator = paginate(request, questions)
    paginator.baseurl = reverse('home') + '?page='
    return render(request, 'index.html', mixin({
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    }))


def index_hot(request):
    questions = Question.objects.popular()
    page, paginator = paginate(request, questions)
    paginator.baseurl = reverse('popular_home') + '?page='
    page.method = 'hot'
    return render(request, 'index.html', mixin({
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    }))

#
# def popular_questions(request):
#     questions = Question.objects.popular()
#     page, paginator = paginate(request, questions)
#     paginator.baseurl = reverse('popular_questions') + '?page='
#     return render(request, 'popular_questions.html', {
#         'questions': page.object_list,
#         'paginator': paginator,
#         'page': page,
#     })


def question(request, pk):
    qst = get_object_or_404(Question, id=pk)
    answers = qst.answer_set.all()
    form = AnswerForm(initial={'question': str(pk)})
    return render(request, 'question_thread.html', mixin({
        'question': qst,
        'answers': answers,
        'form': form,
    }))


def profile(request, pk):
    pass


def tags(request, slug):
    tag = get_object_or_404(Tag, name=slug)
    questions = tag.question.all()
    page, paginator = paginate(request, questions)
    paginator.baseurl = reverse('tags', kwargs={'slug': tag.name}) + '?page='
    return render(request, 'tags_index.html', mixin({
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
        'tag': tag,
    }))


def login_page(request):
     return render(request, 'login.html', mixin({}))


def signup_page(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('home')
            return HttpResponseRedirect(url)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', mixin({
        'form': form
    }))


#@login_required
def ask_question(request):
    if request.method == 'POST' and request.user.is_authenticated():
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            ask = form.save()
            url = reverse('question', args=[ask.id])
            return HttpResponseRedirect(url)
    else:
        form = AskForm()

    return render(request, 'ask_question.html', mixin({
        'form': form
    }))
