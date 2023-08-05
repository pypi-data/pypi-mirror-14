from mangopayments.models import MangoPayTransfer
from decimal import Decimal

def create_mangopay_transfer(debited_wallet, credited_wallet, currency, debited_funds, fees=Decimal('0.0')):
    """
    Create MangoPayTransfer object and transfer money (debited_funds) from credited wallet to debited_wallet.
    If fees are set only (debited_funds - fees) are transferred to debited wallet.
    :param debited_wallet: MangoPayWallet object
    :param credited_wallet: MangoPayWallet
    :param currency: String
    :param debited_funds: Decimal
    :param fees: Decimal. Optional
    :return: MangoPayTransfer object
    """

    transfer = MangoPayTransfer(mangopay_debited_wallet=debited_wallet,
                                mangopay_credited_wallet=credited_wallet,
                                debited_funds=debited_funds,
                                currency=currency,
                                fees=fees)
    transfer.save()
    transfer.create()

    return transfer


