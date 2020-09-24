from django.db import models


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=10, null=False)
    email = models.CharField(max_length=20, null=False)
    d_o_j = models.DateTimeField(blank=True)
    designation = models.CharField(max_length=15, null=False)
    department = models.CharField(max_length=20, null=False)
    salary = models.IntegerField()
    def __str__(self):
        return self.name

class Office(models.Model):
    name = models.CharField(max_length=20)
    branch = models.CharField(max_length=20)
    code = models.IntegerField()
    city = models.CharField(max_length=15)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.branch


class Jobs(models.Model):
    JOB_TYPES = [('remote', '1'),('office', '2')]
    job_type = models.CharField(max_length=10, choices=JOB_TYPES, default='office')
    posted_on = models.DateField()
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.location


class Contact(models.Model):
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=20)
    message = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    productname = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    price = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productname

    class Meta:
        ordering = ['created']

    class Meta:
        db_table = "My_Product"


