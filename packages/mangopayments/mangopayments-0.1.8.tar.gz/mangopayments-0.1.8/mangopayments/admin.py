from django.contrib import admin

# Register your models here.
from mangopayments.models import (MangoPayNaturalUser, MangoPayLegalUser, MangoPayDocument, MangoPayPage,
                                  MangoPayBankAccount, MangoPayWallet, MangoPayPayOut, MangoPayCard,
                                  MangoPayCardRegistration, MangoPayPayIn, MangoPayRefund, MangoPayUser,
                                  MangoPayTransfer)


class MangoPayUserAdmin(admin.ModelAdmin):
    list_display = ("id", "mangopay_id", "user")

class MangoPayNaturalUserAdmin(admin.ModelAdmin):
    list_display = ("id", "mangopay_id", "user", "birthday", "country_of_residence", "nationality", "address", "occupation", "income_range")

class MangoPayLegalUserAdmin(admin.ModelAdmin):
    list_display = ("id", "mangopay_id", "user", "birthday", "country_of_residence", "nationality", "address", "business_name", "generic_business_email", "first_name", "last_name", "headquarters_address", "email")

class MangoPayDocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "mangopay_id", "mangopay_user", "type", "status", "refused_reason_message")

class MangoPayPageAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "file")

class MangoPayBankAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "mangopay_user", "mangopay_id", "iban", "bic", "address")

class MangoPayWalletAdmin(admin.ModelAdmin):
    list_display = ("id", "mangopay_id", "mangopay_user")

class MangoPayPayOutAdmin(admin.ModelAdmin):
    list_display = ("id", "mangopay_id", "mangopay_user", "mangopay_wallet", "mangopay_bank_account", "execution_date", "status", "debited_funds", "fees")

class MangoPayCardAdmin(admin.ModelAdmin):
    list_display = ("id", "mangopay_id", "expiration_date", "alias", "is_active", "is_valid")

class MangoPayCardRegistrationAdmin(admin.ModelAdmin):
    list_display = ("id", "mangopay_id", "mangopay_user", "mangopay_card")

class MangoPayPayInAdmin(admin.ModelAdmin):
    list_display = ("id", "mangopay_id", "mangopay_user", "mangopay_wallet", "mangopay_card", "execution_date", "status", "debited_funds", "fees", "currency", "result_code", "secure_mode_redirect_url")

class MangoPayRefundAdmin(admin.ModelAdmin):
    list_display = ("id", "mangopay_id", "mangopay_user", "debited_funds", "fees", "mangopay_pay_in", "created", "updated", "status", "result_code")

class MangoPayTransferAdmin(admin.ModelAdmin):
    list_display = ("id", "mangopay_id", "mangopay_debited_wallet", "mangopay_credited_wallet", "debited_funds", "fees", "currency", "execution_date", "status", "result_code")

admin.site.register(MangoPayUser, MangoPayUserAdmin)
admin.site.register(MangoPayNaturalUser, MangoPayNaturalUserAdmin)
admin.site.register(MangoPayLegalUser, MangoPayLegalUserAdmin)
admin.site.register(MangoPayDocument, MangoPayDocumentAdmin)
admin.site.register(MangoPayPage, MangoPayPageAdmin)
admin.site.register(MangoPayBankAccount, MangoPayBankAccountAdmin)
admin.site.register(MangoPayWallet, MangoPayWalletAdmin)
admin.site.register(MangoPayPayOut, MangoPayPayOutAdmin)
admin.site.register(MangoPayCard, MangoPayCardAdmin)
admin.site.register(MangoPayCardRegistration, MangoPayCardRegistrationAdmin)
admin.site.register(MangoPayPayIn, MangoPayPayInAdmin)
admin.site.register(MangoPayRefund, MangoPayRefundAdmin)
admin.site.register(MangoPayTransfer, MangoPayTransferAdmin)
