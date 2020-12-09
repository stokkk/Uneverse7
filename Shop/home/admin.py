from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect

from . models import MyModel, IGBTs
from . forms import addIGBTsForm

from django.db import connection

# Register your models here.
class MyAdmin(admin.ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        opts = self.model._meta
        app_label = opts.app_label
        title = opts.verbose_name
        context = {
            'app_label': app_label,
            'title': title
        }
        return render(request, 'home/main-admin.html', context)

    def has_change_permission(self, request, obj=None):
        return not bool(obj)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



class ProductAdmin(admin.ModelAdmin):
    def add_view(self, request, extra_context=None):
        context = {'form': form}
        return render(request, 'home/addIGBTs-admin-panel.html', context=context)

class IGBTsProductAdmin(admin.ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT ps.ID, cg.Name, cns.country_name, brand_name, ps.Name, ps.Price, ps.Discount
        FROM Categories as cg INNER JOIN Products as ps ON (cg.ID = ps.category_id), Brands as b, Countries as cns
        WHERE b.brand_id = ps.brand and cns.id = ps.country_id
        ORDER BY cg.Name ASC
        """)
        products = cursor.fetchall()
        context = {'products': products}
        return render(request, "home/changeIGBTs-admin-panel.html", context=context)

    def has_add_permission(self, request):
        return True

    def add_view(self, request, extra_context=None):
        if request.method == "POST":
            form = addIGBTsForm(request.POST)
            if form.is_valid():
                cursor = connection.cursor()

                category = request.POST['category']
                brand = request.POST['brand']
                name = request.POST['name']
                description = request.POST['description']
                price = request.POST['price']
                discount = request.POST['discount']
                country = request.POST['country']
                count = request.POST['count']
                image_url = request.POST['image_url']

                technology = request.POST['technology']
                builtin_diod = request.POST['builtin_diod']
                icm = request.POST['icm']
                normal_volt = request.POST['normal_volt']
                normal_temperature = request.POST['normal_temperature']
                max_volt = request.POST['max_volt']
                max_amper = request.POST['max_amper']
                max_vat = request.POST['max_vat']
                with connection.cursor() as cursor:
                    # try:
                    cursor.callproc("addIGBTs", [brand, name, description, price, discount, country, category, image_url, count, technology,
                builtin_diod, icm, normal_volt, normal_temperature, max_volt, max_amper, max_vat])
                    # except:
                    #     form = addIGBTsForm()
                    #     return render(request, 'home/addIGBTs-Admin-panel.html', context={'form': form, "error_msg": "Не получилось добавить IGBTs"})
                return HTTPResponseRedirect("/admin/home/igbts/")

        form = addIGBTsForm()
        context = {'form': form}
        return render(request, 'home/addIGBTs-admin-panel.html', context=context)



admin.site.register(MyModel, MyAdmin)
admin.site.register(IGBTs, IGBTsProductAdmin)