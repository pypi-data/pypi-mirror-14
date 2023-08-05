from mangopayments.exceptions import MyException

from mangopayments.models import MangoPayNaturalUser, MangoPayLegalUser, MangoPayBankAccount, MangoPayWallet
from mangopayments.constants import COUNTRY_CHOICES, INCOME_RANGE_CHOICES, BUSINESS



def create_mangopay_natural_user(user, country_of_residence, nationality, birthday, first_name=None, last_name=None,
                                 email=None, address=None, city=None, region=None, postal_code=None, country_code=None,
                                 occupation=None, income_range=None):
    """
    Create MangoPayNaturalUser object.
    :param user: User object
    :param country_of_residence: String. User's country of residence. ISO 3166-1 alpha-2 format is expected
    :param nationality: String. User's nationality. ISO 3166-1 alpha-2 format is expected
    :param birthday: Date. User's birth date.
    :param first_name: String
    :param last_name: String
    :param email: String
    :param address: String. Optional
    :param city: String. Optional
    :param region: String. Optional
    :param postal_code: Integer. Optional
    :param country_code: String. Optional. ISO 3166-1 alpha-2
    :param occupation: String. Optional
    :param income_range: Integer. Optional, one of INCOME_RANGE_CHOICES
    :return: MangoPayNaturalUser object.
    """

    # Check if first_name is given
    if not first_name:
        if user.first_name:
            first_name = user.first_name
        else:
            raise MyException("User's first name is not given.")

    # Check if last_name is given
    if not last_name:
        if user.last_name:
            last_name = user.last_name
        else:
            raise MyException("User's last name is not given.")

    # Check if email is given
    if not email:
        if user.email:
            email = user.email
        else:
            raise MyException("User's email is not given.")

    if country_of_residence not in dict(COUNTRY_CHOICES).keys():
        raise MyException("Country of residence is not valid.")

    if nationality not in dict(COUNTRY_CHOICES).keys():
        raise MyException("Nationality is not valid.")

    if income_range:
        if income_range not in dict(INCOME_RANGE_CHOICES).keys():
            raise MyException("Income range is not valid.")

    # Create MangoPayNaturalUser object.

    mangopay_user = MangoPayNaturalUser(user=user,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        country_of_residence=country_of_residence,
                                        nationality=nationality,
                                        birthday=birthday,
                                        address=address,
                                        city=city,
                                        region=region,
                                        postal_code=postal_code,
                                        country_code=country_code,
                                        occupation=occupation,
                                        income_range=income_range)
    mangopay_user.save()
    mangopay_user.create()

    return mangopay_user


def create_mangopay_legal_user(user, business_name, generic_business_email, country_of_residence, nationality, birthday,
                               first_name=None, last_name=None, email=None, address=None, city=None, region=None,
                               postal_code=None, country_code=None, headquarters_address=None, headquarters_city=None,
                               headquarters_region=None, headquarters_postal_code=None, headquarters_country_code=None):
    """
    Create MangoPayLegalUser object.
    :param user: User object
    :param business_name: string. The name of the company or the organization.
    :param generic_business_email: String. The email of the company or the organization
    :param country_of_residence: String. Legal Representative's country of residence. ISO 3166-1 alpha-2 format is expected
    :param nationality: String. Legal Representative's nationality. ISO 3166-1 alpha-2 format is expected
    :param birthday: Date. Legal Representative's birth date.
    :param first_name: String. Legal Representative's first name.
    :param last_name: String. Legal Representative's last name.
    :param email: String. Optional. Legal Representative's email.
    :param address: String. Optional. Legal Representative's address.
    :param city: String. Optional
    :param region: String. Optional
    :param postal_code: Integer. Optional
    :param country_code: String. Optional. ISO 3166-1 alpha-2
    :param headquarters_address: String. Optional. The address of the company's headquarters.
    :param headquarters_city: String. Optional
    :param headquarters_region: String. Optional
    :param headquarters_postal_code: Integer. Optional
    :param headquarters_country_code: String. Optional. ISO 3166-1 alpha-2
    :return: MangoPayLegalUser object.
    """

    # Check if first_name is given
    if not first_name:
        if user.first_name:
            first_name = user.first_name
        else:
            raise MyException("User's first name is not given.")

    # Check if last_name is given
    if not last_name:
        if user.last_name:
            last_name = user.last_name
        else:
            raise MyException("User's last name is not given.")

    if country_of_residence not in dict(COUNTRY_CHOICES).keys():
        raise MyException("Country of residence is not valid.")

    if nationality not in dict(COUNTRY_CHOICES).keys():
        raise MyException("Nationality is not valid.")


    # Create MangoPayNaturalUser object.

    mangopay_user = MangoPayLegalUser(user=user,
                                      first_name=first_name,
                                      last_name=last_name,
                                      email=email,
                                      country_of_residence=country_of_residence,
                                      nationality=nationality,
                                      birthday=birthday,
                                      address=address,
                                      city=city,
                                      region=region,
                                      postal_code=postal_code,
                                      country_code=country_code,
                                      generic_business_email=generic_business_email,
                                      business_name=business_name,
                                      headquarters_address=headquarters_address,
                                      headquarters_city=headquarters_city,
                                      headquarters_region=headquarters_region,
                                      headquarters_postal_code=headquarters_postal_code,
                                      headquarters_country_code=headquarters_country_code,
                                      type=BUSINESS)
    mangopay_user.save()
    mangopay_user.create()

    return mangopay_user


def create_mangopay_bank_account(mangopay_user, iban, bic, address, city, postal_code, country_code, region=""):
    """
    Create MangoPayBankAccount object.
    :param mangopay_user: MangoPayUser object
    :param iban: String. IBAN Field.
    :param bic: String. BIC Field.
    :param address: String.
    :param city: String
    :param region: String. Optional
    :param postal_code: Integer
    :param country_code: String. ISO 3166-1 alpha-2
    :return: MangoPayBankAccount object
    """

    bank_account = MangoPayBankAccount(mangopay_user=mangopay_user,
                                       iban=iban,
                                       bic=bic,
                                       address=address,
                                       city=city,
                                       region=region,
                                       postal_code=postal_code,
                                       country_code=country_code)
    bank_account.save()
    bank_account.create()

    return bank_account


def create_mangopay_wallet(mangopay_user, currency, description=None):
    """
    Create MangoPayWallet object.
    :param mangopay_user: MangoPayUser object
    :param currency: String
    :param description: String. Wallet's description
    :return: MangoPayWallet object
    """

    # if description is not given set default
    if not description:
        description = "The main wallet."

    mangopay_wallet = MangoPayWallet(mangopay_user=mangopay_user,
                                     currency=currency)
    mangopay_wallet.save()
    mangopay_wallet.create(description=description)

    return mangopay_wallet
