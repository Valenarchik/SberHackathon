import json
from django.shortcuts import render, redirect
from .forms import *


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
    skills_id = [Test_Skills.objects.filter(test_id=t.id) for t in testsList]
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
    return http


def test(request, test_id):
    if request.method == "POST":
        raw_answers = request.body.decode('utf-8').split("&")[0:-1]
        answers = {}
        user_id = request.COOKIES.get('id')
        if not Worker.objects.filter(worker_id=user_id).exists():
            w = Worker.objects.create(worker_id=user_id, experience=5, resume='Резюме', career_status=True)
            w.save()
        else:
            w = Worker.objects.get(worker_id=user_id)

        for answer in raw_answers:
            key, value = answer.split("=")
            answers[int(key)] = int(value)
        test = Test.objects.get(pk=test_id)
        sum_score = 0
        for num, question in enumerate(Test_Question.objects.filter(test_id=test_id)):
            if question.correct_index == answers[num + 1]:
                sum_score += question.score

        Worker_Tests.objects.create(score=sum_score, test_id=test_id, worker_id=w.worker_id).save()
        test_questions = Test_Question.objects.filter(test_id=test)
        http = redirect('/to_employee/success_post')
        return http
    else:
        questions = Test_Question.objects.filter(test_id=test_id)
        variants = [enumerate(q.variants.split('|')) for q in questions]
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


def log_in(request):
    html_page = None
    if request.method == 'POST':
        log_in_form = LogInForm(request.POST)
        if log_in_form.is_valid():
            email = log_in_form.cleaned_data['email']
            password = log_in_form.cleaned_data['password']
            user = User.objects.filter(email=email)
            if user:
                if user.password == password:
                    html_page = redirect('index')
                    html_page.set_cookie('id', f'{user.id}', max_age=None)
                else:
                    context = {'log_in_form': log_in_form}
                    html_page = render(request, 'SlivaJob/login.html', context)
                    log_in_form.add_error('password', 'Неверный пароль')
            else:
                log_in_form.add_error('email', 'Указан неверный E-mail')
    else:
        log_in_form = LogInForm()

    if html_page is None:
        context = {'log_in_form': log_in_form}
        html_page = render(request, 'SlivaJob/login.html', context)
    return html_page


def profile(request):
    context = {}
    id = request.COOKIES.get('id')
    if id:
        user = User.objects.get(id=int(id))
        if request.POST:
            form = ProfileForm(request.POST, instance=user)
            form.save()
        else:
            form = ProfileForm(instance=user)
        context['profile_form'] = form
        html_page = render(request, 'SlivaJob/profile.html', context)
    else:
        html_page = redirect('index')
    return html_page


def vacancies(request):
    return render(request, 'SlivaJob/vacancies.html')


def to_employee(request):
    return render(request, 'SlivaJob/to_employee.html')


def to_employer(request):
    return render(request, 'SlivaJob/to_employer.html')


def to_mentor(request):
    return render(request, 'SlivaJob/to_mentor.html')


def to_orderer(request):
    html_page = None
    id = request.COOKIES.get('id')
    if id:
        orders = Order.objects.filter(id=int(id))

    return html_page


def create_order(request):
    return render(request, 'SlivaJob/create_order.html')


def create_test(request):
    return render(request, 'SlivaJob/create_test.html')


def my_tests(request):
    return render(request, 'SlivaJob/my_tests.html')


def success_post(request):
    return render(request, 'SlivaJob/success_post.html')

