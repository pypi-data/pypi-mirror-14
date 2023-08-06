from distutils.core import setup
setup(
    name = 'copyleaks',
    packages = ['copyleaks'],
    version = '1',
    description = 'Copyleaks API gives you access to a variety of plagiarism detection technologies to protect your online content. Get the most comprehensive plagiarism report for your content that is easy to use and integrate.',
    author = 'Copyleaks ltd',
    author_email = 'support@copyleaks.com',
    url = 'https://api.copyleaks.com', # use the URL to the github repo
    download_url = 'https://github.com/Copyleaks/Python-Plagiarism-Checker', # I'll explain this in a second
    keywords = ['copyleaks', 'api', 'plagiarism', 'content', 'checker', 'online'], # arbitrary keywords
    install_requires=[
        'python-dateutil',
    ],
    classifiers = [],
)