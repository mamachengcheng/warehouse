from django.contrib import admin


from .models import Account,Company

class AccountAdmin(admin.ModelAdmin):
    pass

class CompanyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Account, AccountAdmin)
admin.site.register(Company, CompanyAdmin)
