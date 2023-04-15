from .forms import *

from django.shortcuts import render, redirect


def index(request):
    context = {}
    if request.COOKIES.get('id'):
        context['is_log_in'] = True
    else:
        context['is_log_in'] = False

    return render(request, 'SlivaJob/index.html', context)


def orders(request):
    context = {
        "ordersList": Order.objects.all()
    }
    return render(request, 'SlivaJob/orders.html', context=context)


def workers(request):
    workersList = Worker.objects.all()
    usersList = [User.objects.get(pk=w.worker_id) for w in workersList]
    context = {
        "workersList": zip(workersList, usersList)
    }
    return render(request, 'SlivaJob/workers.html', context=context)


def tests(request):
    testsList = Test.objects.all()
    skills_id = [Test_Skills.objects.filter(test_id=t.id)for t in testsList]
    skills = []
    if len(skills_id) != 0:
        for arr in skills_id:
            skills_arr = [Skill.objects.get(pk=skill.id).name for skill in arr]
            if len(skills_arr) != 0:
                skills.append("\n".join(skills_arr))
    tests = zip(testsList, skills)
    context = {
        'testsList': tests
    }
    http = render(request, 'SlivaJob/tests.html', context)
    #http.set_cookie()
    return http


def test(request, test_id):
    questions = Test_Question.objects.filter(test_id=test_id)
    variants = [q.variants.split('|') for q in questions]
    questionsPairs = zip(questions, variants)
    context = {
        'questions': questionsPairs,
        'test': Test.objects.get(pk=test_id)
    }
    return render(request, f'SlivaJob/test.html', context)
def sign_up(request):
    html_page = None
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            user = sign_up_form.save()
            html_page = redirect('index')
            html_page.set_cookie('id', f'{user.id}', max_age=None)
        else:
            context = {'sing_up_form': sign_up_form}
            html_page = render(request, 'SlivaJob/signup.html', context)
    else:
        sign_up_form = SignUpForm()
        context = {'sing_up_form': sign_up_form}
        html_page = render(request, 'SlivaJob/signup.html', context)
    return html_page


def profile(request):
    context = {}
    html_page = None
    id = request.COOKIES.get('id')
    if id:
        id = int(id)
        user = User.objects.get(id=id)
        form = ProfileForm(instance=user)
        context['profile_form'] = form
        html_page = render(request, 'SlivaJob/profile.html', context);
    else:
        html_page = redirect('index')
    return html_page


def vacancies(request):
    return render(request, 'SlivaJob/vacancies.html')
