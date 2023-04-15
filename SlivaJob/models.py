from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator


class User(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия пользователя")
    third_name = models.CharField(max_length=255, verbose_name="Отчество пользователя", blank=True, null=True)
    photo = models.ImageField(upload_to="media/img/usersPhotos")

    # about = models.TextField(blank=True, default='')

    password = models.CharField(max_length=255, null=True, validators=[MinLengthValidator(8)])
    email = models.EmailField(default='')
    join_date = models.DateTimeField(null=True)
    last_login_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'chart_slug': self.slug})


class Worker(models.Model):
    worker = models.ForeignKey(User, on_delete=models.PROTECT)
    resume = models.TextField(blank=True)
    experience = models.IntegerField(null=False)
    career_status = models.BooleanField(null=False, default=True)


class Mentor(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.TextField(blank=True)


class Orderer(models.Model):
    orderer_id = models.ForeignKey(User, on_delete=models.PROTECT)


class Employer(models.Model):
    employer = models.ForeignKey(User, on_delete=models.PROTECT)
    company_name = models.CharField(max_length=255, verbose_name="Название организации")


class Skill(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название навыка")
    description = models.TextField(blank=True)


class Test(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.PROTECT)
    max_score = models.IntegerField()


class Order(models.Model):
    orderer = models.ForeignKey(Orderer, on_delete=models.PROTECT)
    mentor = models.ForeignKey(Mentor, on_delete=models.PROTECT)
    order_name = models.CharField(max_length=255, verbose_name="Название заказа")
    description = models.TextField(blank=False, null=False)
    score = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    comment = models.TextField(blank=True)


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
