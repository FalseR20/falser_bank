from django.db import models
from django.contrib.auth.models import User


# 0. User из "коробки" - Пользователи

# 1. Клиенты - one-to-one с User (User может и не быть)
class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=30)


# 2. Валюты
class Currencies(models.Model):
    code = models.CharField(max_length=3)


# 3. Курсы валют в разное время
class Courses(models.Model):
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    course_buy = models.BigIntegerField()
    course_sale = models.BigIntegerField()
    change_time = models.TimeField()


# 4. Счета клиентов в разных валютах
class Accounts(models.Model):
    iban = models.CharField(max_length=28, primary_key=True)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=21, decimal_places=6)
    iz_freeze = models.BooleanField()
    clients = models.ManyToManyField(Clients)


# 5. Карты клиентов
class Cards(models.Model):
    number = models.BigIntegerField(primary_key=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=30)
    expiration_date = models.DateField()
    security_code = models.IntegerField()
    iz_freeze = models.BooleanField()


# 6. Операции
class Transactions(models.Model):
    timestamp = models.TimeField()
    sender_iban = models.ForeignKey(User, related_name="sender_iban", on_delete=models.CASCADE)
    receiver_iban = models.ForeignKey(User, related_name="receiver_iban", on_delete=models.CASCADE)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=21, decimal_places=6)
    commission = models.DecimalField(max_digits=21, decimal_places=6)
    description = models.CharField(max_length=50)
    is_successful = models.BooleanField()
