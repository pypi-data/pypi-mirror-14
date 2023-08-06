
from setuptools import setup

setup(name="html2dt",
	version="1.1",
	description="Convert html file to django template file.",
	url="https://github.com/prakash09/html2django_template",
	author="Prakash Kumar",
	author_email="prakash.gbpec@gmail.com",
	license='MIT',
	packages=["html2dt"],
	scripts=["bin/html2dt"],
	zip_safe=False)
