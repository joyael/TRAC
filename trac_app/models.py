from django.db import models

# Create your models here.

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    level = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'roles'  # Specify the table name if it doesn't follow Django's naming convention

    def __str__(self):
        return self.name


class RUser (models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    hashed_password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    class Meta:
        db_table = 'rusers'

    def __str__(self):
        return self.username


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    tag = models.CharField(max_length=255)
    price = models.FloatField()

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name


class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    level = models.IntegerField()

    class Meta:
        db_table = 'permissions'

    def __str__(self):
        return self.name


class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(RUser , on_delete=models.CASCADE, related_name='favourites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favourites')

    class Meta:
        db_table = 'favourites'

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

class RefreshToken(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'refreshtokens'
    
    def __str__(self):
        return f"{self.token[:5]}... {self.check_active()}"
    
    def check_active(self):
        return "Active" if self.is_active else "Not Active"