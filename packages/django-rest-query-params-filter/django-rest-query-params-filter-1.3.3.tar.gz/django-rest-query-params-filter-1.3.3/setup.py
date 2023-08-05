from distutils.core import setup

version = '1.3.3'
app_name = 'django-rest-query-params-filter'
repo = 'https://github.com/jourdanrodrigues/' + app_name

setup(
    name=app_name,
    packages=['query_params_filter'],
    version=version,
    description='Allow your API consumers to make queries through query parameters.',
    author='Jourdan Rodrigues',
    author_email='thiagojourdan@gmail.com',
    url=repo,
    download_url=repo + '/tarball/v' + version,
    keywords=['url', 'filter', 'query', 'params', 'python', 'django', 'rest_framework'],
    classifiers=[],
)
