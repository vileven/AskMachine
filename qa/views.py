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
from django.contrib.auth import authenticate, login, logout
from qa.models import Answer
from qa.models import Question
from qa.models import Profile
from qa.models import Tag, User
from qa.forms import AskForm, AnswerForm, SignUpForm, LoginForm, ProfileForm


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


def profile(request, name, **kwargs):
    user = get_object_or_404(User, username=name)
    prof = Profile.objects.get_profile(user=user)
    if 'success' in request.GET:
        text = request.GET['success']
        return render(request, 'profile.html', mixin({
            'profile': prof,
            'text': text,
        }))
    else:
        return render(request, 'profile.html', mixin({
            'profile': prof,
        }))


@login_required
def profile_edit(request):
    prof = Profile.objects.get_profile(request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(prof)
            url = reverse('profile_page', kwargs={'name': prof.user.username}) + '?success=Every changes saved!'
            return HttpResponseRedirect(url)

    else:
        form = ProfileForm.load(prof)

    return render(request, 'edit_profile.html', mixin({
        'form': form,
        'profile': prof,
    }))


def tags(request, slug):
    tag = get_object_or_404(Tag, name=slug)
    questions = tag.questions.all()
    page, paginator = paginate(request, questions)
    paginator.baseurl = reverse('tags', kwargs={'slug': tag.name}) + '?page='
    return render(request, 'tags_index.html', mixin({
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
        'tag': tag,
    }))


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(request.GET)
            if 'next' in request.GET:
                url = request.GET['next']
            else:
                url = reverse('home')
            print(url)
            return HttpResponseRedirect(url)
    else:
        form = LoginForm()

    if 'success' in request.GET:
        text = request.GET['success']
        return render(request, 'login.html', mixin({
            'form': form,
            'text': text,
        }))

    if 'next' in request.GET:
        return render(request, 'login.html', mixin({
        'form': form,
        'next': request.GET['next']
    }))

    return render(request, 'login.html', mixin({
        'form': form
    }))


def signup_page(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            prof_name = request.POST['login']
            # prof_name = 'Chelsea'
            url = reverse('login_page') \
                  + '?success=Congratulations! Registration completed successfully.'
            return HttpResponseRedirect(url)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', mixin({
        'form': form
    }))


@login_required(login_url='/login/')
def ask_question(request):
    if request.method == 'POST' and request.user.is_authenticated():
        form = AskForm(request.POST)
        if form.is_valid():
            form.profile_user = Profile.objects.get_profile(request.user)
            ask = form.save()
            url = reverse('question', args=[ask.id])
            return HttpResponseRedirect(url)
    else:
        form = AskForm()

    return render(request, 'ask_question.html', mixin({
        'form': form
    }))


def logout_user(request):
    logout(request)
    url = reverse('login_page')
    return HttpResponseRedirect(url)


@login_required
def question_answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.profile_user = Profile.objects.get_profile(request.user)
            answer = form.save()
            url = reverse('question', args=[answer.question.id]) + "#answer_" + str(answer.id)
            return HttpResponseRedirect(url)
    return HttpResponseRedirect('/')
