import json
from django.shortcuts import render, redirect
from .forms import *
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator


def index(request):
    context = {}
    if request.COOKIES.get('id'):
        context['is_log_in'] = True
    else:
        context['is_log_in'] = False

    return render(request, 'SlivaJob/index.html', context)


def orders(request):
    all_orders = []
    user_id = int(request.COOKIES.get('id'))
    w = Worker.objects.create(resume='resume', experience=10, career_status=1, worker_id=user_id)
    w.save()
    worker = Worker.objects.get(worker_id=w.worker_id)
    worker_skills_id = Worker_Skills.objects.filter(worker_id=worker.id)
    for order in Order.objects.all():
        for skills in Skills_Orders.objects.filter(order_id=order.id):
            current_skills_id = [skill.id for skill in skills]
            for worker_skill_id in worker_skills_id:
                if current_skills_id.__contains__(worker_skill_id):
                    all_orders.append(order)
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
        print(user_id)
        if not Worker.objects.filter(worker_id=user_id).exists():
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            w = Worker.objects.create(worker_id=user_id, experience=5, resume='Резюме', career_status=True)
            w.save()
        else:
            print("------------------------------------------------------")
            w = Worker.objects.get(worker_id=user_id)
        print(w.worker_id)
        for answer in raw_answers:
            key, value = answer.split("=")
            answers[int(key)] = int(value)
        test = Test.objects.get(pk=test_id)
        sum_score = 0
        for question in Test_Question.objects.filter(test_id=test_id):
            if question.correct_index == answers[question.local_index]:
                sum_score += question.score
        Worker_Tests.objects.create(score=sum_score, test_id=test_id, worker_id=w.pk).save()
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
    context = {}
    id = request.COOKIES.get('id')
    if id:
        testsList = Test.objects.filter(mentor=id)
        context['testsList'] = testsList
        return render(request, 'SlivaJob/to_mentor.html', context)
    else:
        return redirect('index')


def to_orderer(request):
    html_page = None
    id = request.COOKIES.get('id')
    context = {}
    if id:
        filt = None
        if request.POST:
            filter_form = FilterOrderForm(request.POST)
            if filter_form.is_valid():
                filt = filter_form.cleaned_data['status']
        else:
            filter_form = FilterOrderForm()

        if filt is not None and filt != '-1':
            orders = Order.objects.filter(orderer=int(id), score=filt)
        else:
            orders = Order.objects.filter(orderer=int(id))
        if len(orders) == 0:
            context['is_empty'] = True
        context['filter_form'] = filter_form
        context['orders'] = orders
        html_page = render(request, 'SlivaJob/to_orderer.html', context)
    else:
        html_page = redirect('index')

    return html_page


def create_order(request):
    id = int(request.COOKIES.get('id'))
    if request.POST:
        create_order_form = CreateOrderForm(request.POST)
        if create_order_form.is_valid():
            order_name = create_order_form.cleaned_data['order_name']
            description = create_order_form.cleaned_data['description']
            score = create_order_form.cleaned_data['score']
            comment = create_order_form.cleaned_data['comment']
            order = Order.objects.create(
                orderer=User.objects.get(id=id),
                order_name=order_name,
                description=description,
                score=score,
                comment=comment,
                status=0
            )
            order.save()
            return redirect('to_orderer')
        else:
            context = {'create_order_form': create_order_form}
            return render(request, 'SlivaJob/create_order.html', context)

    else:
        create_order_form = CreateOrderForm()
        context = {'create_order_form': create_order_form}
        return render(request, 'SlivaJob/create_order.html', context)


def create_test(request):
    id = int(request.COOKIES.get('id'))
    if request.POST:
        create_test_form = CreateTestForm(request.POST)
        if create_test_form.is_valid():
            name = create_test_form.cleaned_data['name']
            test = Test.objects.create(mentor=User.objects.get(id=id), name=name)
            test.save()
            return redirect('to_mentor')
    else:
        create_test_form = CreateTestForm()
    context = {
        'form': create_test_form
    }
    return render(request, 'SlivaJob/create_test.html', context=context)


def show_test(request, test_id):
    questions = Test_Question.objects.filter(test_id=test_id)
    variants = [q.variants.split('|') for q in questions]
    questionsPairs = zip(questions, variants)
    context = {
        'questions': questionsPairs,
        'test': Test.objects.get(pk=test_id)
    }
    return render(request, 'SlivaJob/show_test.html', context)


def create_question(request, test_id):
    context = {}
    if request.POST:
        create_question_form = CreateQuestionForm(request.POST)
        if create_question_form.is_valid():
            question = create_question_form.cleaned_data['question']
            answer1 = create_question_form.cleaned_data['answer1']
            answer2 = create_question_form.cleaned_data['answer2']
            answer3 = create_question_form.cleaned_data['answer3']
            answer4 = create_question_form.cleaned_data['answer4']
            arr = [answer1, answer2, answer3, answer4]
            answers = '|'.join(arr)
            rightAnswerIndex = create_question_form.cleaned_data['right_answer']
            correct = arr[rightAnswerIndex - 1]
            question = Test_Question.objects.create(test_id=test_id, question=question, variants=answers,
                                                    correct_index=rightAnswerIndex, correct=correct)
            question.save()
            return redirect('show_test', test_id=test_id)
    else:
        create_question_form = CreateQuestionForm()
    context['create_question_form'] = create_question_form
    return render(request, 'SlivaJob/create_question.html', context)


def my_tests(request):
    return render(request, 'SlivaJob/my_tests.html')


def success_post(request):
    return render(request, 'SlivaJob/success_post.html')


def test_page(request):
    form = FilterOrderForm()
    return render(request, 'SlivaJob/test_page.html', {'form': form})
