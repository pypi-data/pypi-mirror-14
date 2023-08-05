from mangopayments.models import MangoPayCardRegistration, MangoPayPayInByCard



def create_mangopay_card_registration(mangopay_user, currency, card_type=None):
    """
    Create MangoPayCardRegistration object. The returned preregistration data is served to client side in order to create MangoPayCard.
    At the same time MangoPayCard object is created - it needs to be updated with mangopay_id obtained from MangoPay server by the client.
    :param mangopay_user: MangoPayUser object
    :param currency: String
    :param card_type: string ("CB_VISA_MASTERCARD" or "MAESTRO")
    :return: dict. {"access_key": "",
                    "card_registration_URL": "",
                    "preregistration_data": "",
                    "card_registration_id": 2
                   }
    """

    card_registration = MangoPayCardRegistration(mangopay_user=mangopay_user)
    card_registration.save()
    card_registration.create(currency, card_type)

    data = card_registration.get_preregistration_data()
    access_key = data['accessKey']
    card_registration_URL = data['cardRegistrationURL']
    preregistration_data = data['preregistrationData']
    card_registration_id = card_registration.mangopay_id

    return {"access_key": access_key,
            "card_registration_URL": card_registration_URL,
            "preregistration_data": preregistration_data,
            "card_registration_id": card_registration_id}


def update_mangopay_card_with_mangopay_id(mangopay_card_registration_id, mangopay_card_id):
    """
    Given mangopay_card_registration_id find MangoPayCardRegistration object and its MangoPayCard object, which needs to be updated.
    :param mangopay_card_registration_id: integer
    :param mangopay_card_id: integer
    :return: updated MangoPayCard object
    """

    card_registration = MangoPayCardRegistration.objects.get(mangopay_id=mangopay_card_registration_id)
    card = card_registration.mangopay_card

    card_registration.save_mangopay_card_id(mangopay_card_id)

    # update other info
    card.request_card_info()
    card.save()

    return card


def create_mangopay_payin(mangopay_user, mangopay_wallet, mangopay_card, debited_funds, fees, currency, secure_mode_return_url):
    """
    Create a payin from card to user's wallet.
    :param mangopay_user: MangoPayUser object
    :param mangopay_wallet: MangoPayWallet object
    :param mangopay_card: MangoPayCard
    :param debited_funds: Decimal
    :param fees: Decimal
    :param currency: String
    :param secure_mode_return_url: URL
    :return: MangoPayPayInByCard object
    """

    payin = MangoPayPayInByCard(mangopay_user=mangopay_user,
                                mangopay_wallet=mangopay_wallet,
                                mangopay_card=mangopay_card,
                                debited_funds=debited_funds,
                                currency=currency,
                                fees=fees)
    payin.save()
    payin.create(secure_mode_return_url=secure_mode_return_url)

    return payin
