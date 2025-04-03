from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.forms import inlineformset_factory

def home(request):
    Activities = ACTIVITY.objects.all()
    news = NEWS.objects.all()
    return render(request, 'home.html', {'Activities': Activities, 'News': news, 'lenght':len(news)})

def admin_only(user):
    return user.is_superuser or user.is_staff

@user_passes_test(admin_only)
def signUp(request):
    if request.method == 'POST':
        form = Signupform(request.POST)
        if form.is_valid():
            form.save()
            print(form)
        else:
            print(form.errors)
    else:
        form = Signupform()
    return render(request, 'register.html', {'form':form})

User = get_user_model()
def logIn(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = CustomLoginForm(request.POST)
            if form.is_valid():
                unique_code = form.cleaned_data['unique_code']
                password = form.cleaned_data['password']
                try:
                    user = User.objects.get(unique_code=unique_code)
                    if user.check_password(password):
                        login(request, user)
                        return redirect('home')
                    else:
                        messages.error(request, "Invalid password.")
                except User.DoesNotExist:
                    messages.error(request, "Invalid code.")
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return render(request, 'home.html')

@login_required(login_url='login')
def activity(request, activity_id):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        Code = request.POST.get('Code')
        activity_name = request.POST.get('activity')
        user_class = request.POST.get('class')
        subscriber = SubscribeModel.objects.create(name=username, Code=Code, activity=activity_name, user_class=user_class)
        if Code in USER.objects.values_list('unique_code', flat=True):
            subscriber.save()
        else:
            error = 'code is incorrect'
            subscriber.delete()
    activity = get_object_or_404(ACTIVITY, id=activity_id)
    return render(request, 'activity.html', {'activity':activity, 'error':error})

@login_required(login_url='login')
def PodCasts(request):
    Podcasts = PODCAST.objects.all()
    return render(request, 'podcasts.html', {'Podcasts':Podcasts})

@login_required(login_url='login')
def PodCast(request, pod_id):
    Podcast = get_object_or_404(PODCAST, id=pod_id)
    return render(request, 'podcast.html', {'Podcast': Podcast})

@login_required(login_url='login')
@user_passes_test(admin_only)
def SyStEm(request):
    # subs = SubscribeModel.objects.all()
    subs = SubscribeModel.objects.filter(activity = ' ')
    if request.method == 'GET':
        if 'activity_title' in request.GET :
            name = request.GET.get('activity_select')
            subs = SubscribeModel.objects.filter(activity = name)
    else:
        if 'crt_activity' in request.POST :
            title = request.POST.get('title')
            brief = request.POST.get('brief')
            details = request.POST.get('details')

            activity = ACTIVITY.objects.create(title=title, brief=brief, details=details)
            activity.save()
        
        if 'crt_eps' in request.POST :
            title = request.POST.get('title')
            vid = request.FILES.get('vid')

            P_epsoid = PODCAST.objects.create(name=title, video=vid)
            P_epsoid.save()

        elif 'crt_new' in request.POST :
            title = request.POST.get('title') 
            text = request.POST.get('text')
            pic = request.FILES.get('pic')

            New = NEWS.objects.create(title=title, text=text, pic=pic)
            New.save()

    activites1 = ACTIVITY.objects.all()
    activites2 = ACTIVITY.objects.all()

    Epsoids = PODCAST.objects.all()
    News = NEWS.objects.all()

    return render(request, 'system.html', {'activites1':activites1, 'activities2':activites2, 'Epsoids':Epsoids, 'News':News, 'subs':subs})

@user_passes_test(admin_only)
def DeLeTe(request):
    if request.method == 'POST':
        if 'del_activity' in request.POST :
            title = request.POST.get('activities') 
            activity = ACTIVITY.objects.filter(title=title)
            activity.delete()

        elif 'del_eps' in request.POST :
            name = request.POST.get('epsoids')
            epsoid = PODCAST.objects.filter(name=name)
            epsoid.delete()
        
        elif 'del_new' in request.POST :
            text = request.POST.get('news')
            new = NEWS.objects.filter(text=text)
            new.delete()

    return redirect('sstm')

@user_passes_test(admin_only)
def UpDaTe(request):
    if request.method == 'POST':
        if 'upd_act' in request.POST :
            ori_title = request.POST.get('ori-title')
            title = request.POST.get('title')
            brief = request.POST.get('brief')
            details = request.POST.get('details')
            
            activity = get_object_or_404(ACTIVITY, title=ori_title)
            
            if title:
                activity.title = title
            if brief:
                activity.brief = brief
            if details:
                activity.details = details
            activity.save()

        elif 'upd_eps' in request.POST :
            ori_title = request.POST.get('ori-title')
            title = request.POST.get('title')
            vid = request.FILES.get('vid')
            
            epsoid = get_object_or_404(PODCAST, name=ori_title)
            
            if title:
                epsoid.name = title
            if vid:
                epsoid.video = vid
            epsoid.save()
        
        elif 'upd_new' in request.POST :
            ori_title = request.POST.get('ori-title')
            title = request.POST.get('title')
            text = request.POST.get('text')
            pic = request.FILES.get('pic')
            
            news = get_object_or_404(NEWS, title=ori_title)
            
            if title:
                news.title = title
            if text:
                news.text = text
            if pic:
                news.pic = pic
            news.save()

    return redirect('sstm')

@user_passes_test(admin_only)
def create_article(request):
    articles = ARTICLE.objects.all()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_article')
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form, 'articles':articles})

@login_required(login_url='login')
def Articles(request):
    Articles = ARTICLE.objects.all()
    return render(request, 'articles.html', {'Articles':Articles})

@login_required(login_url='login')
def Article(request, art_id):
    Article = get_object_or_404(ARTICLE, id=art_id)
    return render(request, 'article.html', {'Article': Article})


@user_passes_test(admin_only)
def create_quiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            return redirect('add_questions', quiz_id=quiz.id)

    else:
        form = QuizForm()

    return render(request, 'create_quiz.html', {'form': form})


@user_passes_test(admin_only)
def add_questions(request, quiz_id):
    quiz = QUIZ.objects.get(id=quiz_id)
    QuestionFormSet = inlineformset_factory(QUIZ, QUESTION, fields=('text',), extra=quiz.num_questions)

    if request.method == "POST":
        formset = QuestionFormSet(request.POST, instance=quiz)
        if formset.is_valid():
            formset.save()
            return redirect('add_answers', quiz_id=quiz.id)

    else:
        formset = QuestionFormSet(instance=quiz)

    return render(request, 'add_questions.html', {'formset': formset})


@user_passes_test(admin_only)
def add_answers(request, quiz_id):
    quiz = QUIZ.objects.get(id=quiz_id)
    questions = quiz.questions.all()

    if request.method == "POST":
        for question in questions:
            for i in range(1, 5):
                answer_text = request.POST.get(f'answer_{question.id}_{i}')
                is_correct = request.POST.get(f'correct_{question.id}') == str(i)

                ANSWER.objects.create(question=question, text=answer_text, is_correct=is_correct)

        return redirect('create_quiz')

    return render(request, 'add_answers.html', {'quiz': quiz, 'questions': questions})


@login_required(login_url='login')
def take_quiz(request, article_title):
    try:
        article = ARTICLE.objects.get(title=article_title)
        quiz = QUIZ.objects.get(title=article)
    except ARTICLE.DoesNotExist:
        return HttpResponse("Article not found", status=404)
    except QUIZ.DoesNotExist:
        return HttpResponse("Quiz not found", status=404)

    questions = quiz.questions.prefetch_related('answers')

    if request.method == "POST":
        score = 0
        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                answer = ANSWER.objects.get(id=selected_answer_id)
                if answer.is_correct:
                    score += 1

        return render(request, 'quiz_result.html', {'quiz': quiz, 'score': score, 'total': quiz.questions.count()})

    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})

@user_passes_test(admin_only)
def search_Users(request):
    query = request.GET.get('q', '')
    if query :
        users = USER.objects.filter(username__icontains=query
            ) | USER.objects.filter(Level__icontains=query
            ) | USER.objects.filter(unique_code__icontains=query
            ) | USER.objects.filter(user_class__icontains=query)
    else:
        users = USER.objects.all()
    return render(request, 'Search_Users.html', {'users': users})

@user_passes_test(admin_only)
def delete_Users(request, user_code):
    if request.user.is_superuser:
        user = get_object_or_404(USER, unique_code=user_code)
        user.delete()
        return redirect('search-users')
    else:
        return HttpResponseForbidden("You are not allowed to delete this user.")

@user_passes_test(admin_only)
def delete_Articles(request, article_title):
    if request.user.is_superuser:
        article = get_object_or_404(ARTICLE, title=article_title)
        article.delete()
        return redirect('create_article')
    else:
        return HttpResponseForbidden("You are not allowed to delete this article.")