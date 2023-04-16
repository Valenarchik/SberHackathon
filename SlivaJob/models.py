import datetime

from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator


class User(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия пользователя")
    third_name = models.CharField(max_length=255, verbose_name="Отчество пользователя", blank=True, null=True)
    photo = models.ImageField(upload_to="media/img/usersPhotos")

    password = models.CharField(max_length=255, null=False, validators=[MinLengthValidator(8)], verbose_name="Пароль",
                                default="12345678")
    email = models.EmailField(default="defaultemail@mail.ru")
    join_date = models.DateTimeField(null=False, auto_now_add=True)
    last_login_date = models.DateTimeField(null=False, default=datetime.datetime.now())
    is_active = models.BooleanField(null=False, default=False)


class Worker(models.Model):
    worker = models.ForeignKey(User, on_delete=models.PROTECT)
    resume = models.TextField(blank=True)
    experience = models.IntegerField(null=False)
    career_status = models.BooleanField(null=False, default=True)


class Mentor(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.TextField(blank=True)


class Orderer(models.Model):
    orderer = models.ForeignKey(User, on_delete=models.PROTECT)


class Employer(models.Model):
    employer = models.ForeignKey(User, on_delete=models.PROTECT)
    company_name = models.CharField(max_length=255, verbose_name="Название организации")


class Skills_Group(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название группы навыков")


class Skill(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название навыка")
    description = models.TextField(blank=True)
    group = models.ForeignKey(Skills_Group, on_delete=models.PROTECT)


class Test(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, verbose_name="Название теста", default="Test name")


class Test_Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.PROTECT)
    question = models.TextField(blank=False, default="Вопрос не задан")
    variants = models.TextField(blank=False, default="Вариант ответа")
    correct_index = models.IntegerField(default=0)
    #ocal_index = models.IntegerField(default=0, unique=True)
    correct = models.TextField(default="Правильный вариант ответа")
    score = models.IntegerField(default=1)


class Order(models.Model):
    orderer = models.ForeignKey(User, on_delete=models.PROTECT)
    order_name = models.CharField(max_length=255, verbose_name="Название заказа")
    description = models.TextField(blank=False, null=False)
    score = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    comment = models.TextField(blank=True)
    status = models.IntegerField(default=0)


class Test_Skills(models.Model):
    test = models.ForeignKey(Test, on_delete=models.PROTECT)
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT)


class Worker_Tests(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT)
    test = models.ForeignKey(Test, on_delete=models.PROTECT)
    score = models.IntegerField()


class Worker_Skills(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT)
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT)


class Skills_Orders(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)


class Workers_Orders(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
