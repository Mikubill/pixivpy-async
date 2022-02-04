import re
import setuptools

with open('README.md', 'rt', encoding='utf-8') as f:
    long_description = f.read()

with open('pixivpy_async/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

setuptools.setup(
    name='PixivPy-Async',
    version=version,
    description='Pure Python 3 Async Pixiv API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Mikubill/pixivpy-async',
    author='Mikubill',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    keywords=['pixiv', 'api', 'pixivpy', 'pixivpy_async'],
    packages=['pixivpy_async'],
    install_requires=['aiohttp', 'aiofiles', 'deprecated'],
    extra_requires={
        'socks': [
            'aiohttp_socks',
        ],
        'speedups': [
            'aiohttp[speedups]'
        ]
    },
    python_requires='>=3.5.3',
)
