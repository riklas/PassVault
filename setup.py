try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'stores pgp encrypted passwords',
    'author': 'rikin',
    'url': 'https://github.com/riklas/passVault',
    # 'download_url': 'Where to download it.',
    'author_email': 'rikin_daya_s@hotmail.com',
    'version': '0.1',
    # 'install_requires': ['argparse'],
    # 'dependency_links': ['https://github.com/asweigart/pyperclip/tarball/master']
    'packages': ['passVault'],
    'scripts': ['bin/passVaultSetup.sh'],
    'name': 'passVault'
}

setup(**config)
