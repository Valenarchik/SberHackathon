from django.db import models


# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")


class Worker(models.Model):
    worker_id = models.ForeignKey(User, on_delete=models.PROTECT)


class Mentor(models.Model):
    mentor_id = models.ForeignKey(User, on_delete=models.PROTECT)


class Orderer(models.Model):
    orderer_id = models.ForeignKey(User, on_delete=models.PROTECT)


class Employer(models.Model):
    employer_id = models.ForeignKey(User, on_delete=models.PROTECT)


class Skill(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название навыка")
    description = models.TextField(blank=True)


class Test(models.Model):
    mentor_id = models.ForeignKey(Mentor, on_delete=models.PROTECT)


class Order(models.Model):
    orderer_id = models.ForeignKey(Orderer, on_delete=models.PROTECT)
    mentor_id = models.ForeignKey(Mentor, on_delete=models.PROTECT)


class Worker_Tests(models.Model):
    worker_id = models.ForeignKey(Worker, on_delete=models.PROTECT)
    test_id = models.ForeignKey(Test, on_delete=models.PROTECT)


class Worker_Skills(models.Model):
    worker_id = models.ForeignKey(Worker, on_delete=models.PROTECT)
    skill_id = models.ForeignKey(Skill, on_delete=models.PROTECT)


class Skills_Orders(models.Model):
    skill_id = models.ForeignKey(Skill, on_delete=models.PROTECT)
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT)

class Workers_Orders(models.Model):
    worker_id = models.ForeignKey(Worker, on_delete=models.PROTECT)
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT)
