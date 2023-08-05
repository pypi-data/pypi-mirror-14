from distutils.core import setup
setup(
  name = 'mangopayments',
  packages = ['mangopayments','mangopayments/migrations', 'mangopayments/helpers'],
  package_data={'mangopayments':['templates/*', 'static/mangopayments/js/*']},
  version = '0.1.8',
  description = 'A Django app for processing MangoPay transactions.',
  author = 'Polona Tomasic',
  author_email = 'polona@olaii.com',
  url = 'https://gitlab.xlab.si/olaii/olaii-mangopay', # use the URL to the github repo
  download_url = 'https://gitlab.xlab.si/olaii/olaii-mangopay/tree/0.1.8',
  keywords = ['mangopay'], # arbitrary keywords
  classifiers = [],
)
