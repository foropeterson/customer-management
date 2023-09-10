from django.db import models
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput
from django import forms

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=20, blank=True, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name
class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    ) 

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)  # Added image field
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)


def __str__(self):
		return self.name

class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)

	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return self.product.name
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email','phone']  # Add other fields as needed

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}), 
            # Add more field widgets as needed
        }
        labels = {
            'name': 'Name',
            'email': 'Email',
            'phone': 'Phone',
            # Add more field labels as needed
		}
