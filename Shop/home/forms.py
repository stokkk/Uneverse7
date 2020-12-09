from django import forms
from django.contrib.auth.models import User
from . models import IGBTs, Product

from django.db import connection

# my forms

class RegistrationForm(forms.ModelForm):
    login = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, max_length=50)
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = "Ваш логин"
        self.fields['password'].label = "Ваш пароль"
        self.fields['confirm_password'].label = "Повторите пароль"

    def clean_login(self):
        username_ = self.cleaned_data['login']
        if User.objects.filter(username=username_).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")

    def clean(self):
        password1_ = self.cleaned_data['password']
        password2_ = self.cleaned_data['confirm_password']
        if password1_ != password2_:
            raise forms.ValidationError("Пароли не совпадают")
        return self.cleaned_data


    class Meta:
        model = User
        fields = ['login', 'password', 'confirm_password']

class LogInForm(forms.ModelForm):
    login = forms.CharField(label="Логин", max_length=50)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput, max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = "Ваш логин"
        self.fields['password'].label = "Ваш пароль"


    def clean_login(self):
        username_ = self.cleaned_data['login']
        if not User.objects.filter(username=username_).exists():
            raise ValueError("Пользователя с таким именем не существует")

    class Meta:
        model = User
        fields = ['login', 'password']

def run_query(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()

class addProductForm(forms.ModelForm):
    
    category = forms.ChoiceField(
        choices=
            tuple(i[0] for i in (tuple(zip(ct,ct)) for ct in run_query("""SELECT ct.Name FROM Categories as ct WHERE ct.ID NOT IN (SELECT ParentID FROM Categories WHERE ParentID IS NOT NULL)""")))
    )
    brand = forms.ChoiceField(
        choices=
            tuple(i[0] for i in (tuple(zip(brand,brand)) for brand in run_query("SELECT brand_name FROM Brands")))
    )
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=500,widget=forms.Textarea)
    price = forms.FloatField()
    discount = forms.FloatField()
    country = forms.ChoiceField(
        choices=
            tuple(i[0] for i in (tuple(zip(cy,cy)) for cy in run_query("SELECT country_name FROM Countries")))
        )
    count = forms.IntegerField()
    image_url = forms.CharField(max_length=255)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label = "Категория"
        self.fields['brand'].label = "Брэнд"
        self.fields['name'].label = "Название товара"
        self.fields['description'].label = "Описание товара"
        self.fields['price'].label = "Цена"
        self.fields['discount'].label = "Цена со скидкой"
        self.fields['country'].label = "Страна производства"
        self.fields['count'].label = "Количество товара на складе"
        self.fields['image_url'].label = "URL картинки"
    class Meta:
        model = Product 
        fields = ['name', 'country', 'brand', 'price', 'discount', 'image_url', 'count', 'description']


class addIGBTsForm(addProductForm):
    technology = forms.CharField(max_length=30)
    builtin_diod = forms.BooleanField()
    icm = forms.FloatField()
    normal_volt = forms.FloatField()
    normal_temperature = forms.FloatField()
    max_volt = forms.FloatField()
    max_amper = forms.FloatField()
    max_vat = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['technology'].label = "Технология"
        self.fields['builtin_diod'].label = "Встроенный диод"
        self.fields['icm'].label = "ICM"
        self.fields['normal_volt'].label = "Вольт в нормальном стостоянии"
        self.fields['normal_temperature'].label = "Температура в нормальном состоянии"
        self.fields['max_volt'].label = "Максимальное напряжение В."
        self.fields['max_amper'].label = "Максимальная сила тока А."
        self.fields['max_vat'].label = "Максимальная мощность Вт."

    class Meta:
        model = IGBTs
        fields = ['technology', 'builtin_diod', 'icm', 'normal_volt', 'normal_temperature', 'max_volt', 'max_amper', 'max_vat']
