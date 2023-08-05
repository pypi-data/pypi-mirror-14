from datetime import datetime, timedelta

from django.conf import settings
from celery import shared_task
from celery.task import PeriodicTask
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from mangopaysdk.types.exceptions.responseexception import ResponseException

from .constants import VALIDATION_ASKED

logger = get_task_logger(__name__)



@shared_task(bind=True, default_retry_delay=5*60, max_retries=10)
def create_mangopay_user(self, mangopay_user):
    """
    :param mangopay_user: MangoPayNaturalUser or MangoPayLegalUser object
    """
    try:
        # make sure not to create multiple users for one MangoPayUser
        if not mangopay_user.mangopay_id:
            mangopay_user.create()
        else:
            logger.error("MangoPayUser with id %s has already been created." % mangopay_user.id)
    except ResponseException as exc:
         logger.error("Could not create MangoPayUser with id %s. Error: %s" % (mangopay_user.id, exc))


@shared_task(bind=True, default_retry_delay=5*60, max_retries=10)
def update_mangopay_user(self, mangopay_user):
    """
    :param mangopay_user: MangoPayNaturalUser or MangoPayLegalUser object
    """
    try:
        # make sure this MangoPayUser has been created
        if mangopay_user.mangopay_id:
            mangopay_user.update()
        else:
            logger.error("MangoPayUser with id %s has not been created yet." % mangopay_user.id)
    except ResponseException as exc:
        logger.error("Could not update MangoPayUser with id %s. Error: %s" % (mangopay_user.id, exc))


@shared_task(bind=True, default_retry_delay=5*60, max_retries=10)
def create_mangopay_bank_account(self, mangopay_bank_account):
    """
    :param mangopay_bank_account: MangoPayBankAccount object
    """
    try:
        # make sure the MangoPayUser who owns the bank account has already been created
        if not mangopay_bank_account.mangopay_user.mangopay_id:
            logger.error("MangoPayUser with id %s that owns MangoPayBankAccount has not been created yet." % mangopay_bank_account.mangopay_user.id)
        else:
            # make sure not to create multiple bank accounts for one MangoPayBankAccount
            if not mangopay_bank_account.mangopay_id:
                mangopay_bank_account.create()
            else:
                logger.error("MangoPayBankAccount with id %s has already been created." % mangopay_bank_account.id)
    except ResponseException as exc:
         logger.error("Could not create MangoPayBankAccount with id %s. Error: %s" % (mangopay_bank_account.id, exc))


@shared_task(bind=True, default_retry_delay=5*60, max_retries=10)
def create_mangopay_wallet(self, mangopay_wallet, description):
    try:
        # make sure the MangoPayUser who owns the wallet has already been created
        if not mangopay_wallet.mangopay_user.mangopay_id:
            logger.error("MangoPayUser with id %s that owns MangoPayWallet has not been created yet." % mangopay_wallet.mangopay_user.id)
        else:
            # make sure not to create multiple wallets for one MangoPayWallet
            if not mangopay_wallet.mangopay_id:
                mangopay_wallet.create(description)
            else:
                logger.error("MangoPayWallet with id %s has already been created." % mangopay_wallet.id)
    except ResponseException as exc:
         logger.error("Could not create MangoPayWallet with id %s. Error: %s" % (mangopay_wallet.id, exc))



@shared_task(bind=True, default_retry_delay=5*60, max_retries=10)
def create_mangopay_transfer(self, mangopay_transfer):
    try:
        # make sure the credited MangoPayWallet has already been created
        if not mangopay_transfer.mangopay_credited_wallet.mangopay_id:
            logger.error("The credited MangoPayWallet with id %s has not been created yet." % mangopay_transfer.mangopay_credited_wallet.id)
        elif not mangopay_transfer.mangopay_debited_wallet.mangopay_id:
            logger.error("The debited MangoPayWallet with id %s has not been created yet." % mangopay_transfer.mangopay_debited_wallet.id)
        else:
            # make sure not to create multiple transfers for one MangoPayTransfer
            if not mangopay_transfer.mangopay_id:
                mangopay_transfer.create()
            else:
                logger.error("MangoPayTransfer with id %s has already been created." % mangopay_transfer.id)
    except ResponseException as exc:
         logger.error("Could not create MangoPayTransfer with id %s. Error: %s" % (mangopay_transfer.id, exc))


'''
def next_weekday():
    def maybe_add_day(date):
        if datetime.weekday(date) >= 5:
            date += timedelta(days=1)
            return maybe_add_day(date)
        else:
            return date
    return maybe_add_day(datetime.now() + timedelta(days=1))

# TODO
@shared_task(bind=True, default_retry_delay=5*60, max_retries=10)
def create_mangopay_document_and_pages_and_ask_for_validation(id):
    document = MangoPayDocument.objects.get(
        id=id, mangopay_id__isnull=True, type__isnull=False)
    try:
        document.create()
    except ResponseException as exc:
        raise create_mangopay_document_and_pages_and_ask_for_validation.retry(
            (), {"id": id}, exc=exc)
    for page in document.mangopay_pages.all():
        page.create()
    document.ask_for_validation()


@shared_task(bind=True, default_retry_delay=5*60, max_retries=10)
def update_document_status(id):
    document = MangoPayDocument.objects.get(id=id)
    if document.status == VALIDATION_ASKED:
        document.get()


class UpdateDocumentsStatus(PeriodicTask):
    abstract = True
    run_every = crontab(minute=0, hour='8-17', day_of_week='mon-fri')

    def run(self, *args, **kwargs):
        documents = MangoPayDocument.objects.filter(status=VALIDATION_ASKED)
        for document in documents:
            update_document_status.delay(document.id)

@shared_task(bind=True, default_retry_delay=5*60, max_retries=10)
def create_mangopay_pay_out(id, tag=''):
    payout = MangoPayPayOut.objects.get(id=id, mangopay_id__isnull=True)
    try:
        payout.create(tag)
    except ResponseException as exc:
        kwargs = {"id": id, "tag": tag}
        raise create_mangopay_pay_out.retry((), kwargs, exc=exc)
    eta = next_weekday()
    update_mangopay_pay_out.apply_async((), {"id": id}, eta=eta)


@shared_task(bind=True, default_retry_delay=5*60, max_retries=10)
def update_mangopay_pay_out(id):
    payout = MangoPayPayOut.objects.get(id=id, mangopay_id__isnull=False)
    try:
        payout = payout.get()
    except ResponseException as exc:
        raise update_mangopay_pay_out.retry((), {"id": id}, exc=exc)
    if not payout.status or payout.status == "CREATED":
        eta = next_weekday()
        update_mangopay_pay_out.apply_async((), {"id": id}, eta=eta)
    elif payout.status == "SUCCEEDED":
        task = getattr(settings, 'MANGOPAY_PAYOUT_SUCCEEDED_TASK', None)
        if task:
            task().run(payout_id=payout.id)
    else:
        logger.error("Payout %i could not be process successfully" % payout.id)
'''

