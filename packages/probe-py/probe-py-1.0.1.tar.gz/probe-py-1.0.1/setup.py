# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "probe-py"
VERSION = "1.0.1"



# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.10", "six >= 1.9", "certifi", "python-dateutil"]

setup(
    name="probe-py",
    version=VERSION,
    description="Probe API Client",
    author_email="suraj@loanzen.in",
    url="https://github.com/loanzen/probe-py",
    keywords=["Probe API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Probe provides you access to information on all companies in India.\nData collected, cleaned and curated from multiple sources is made\navailable through our APIs now.\n\n\nCome experience and build something awesome!\n\n\n\nAll endpoints are accessible only via https and are located at `api.probe42.in`\n\n\n## Authentication\nOnce you&#39;ve  [registered your client](http://developer.probe42.in) it&#39;s easy to start requesting data from Probe.\nYou will be issued automatically an API key, which you can provide in all your calls.\n\nIt is very important to keep your API key as a secret and store it in a\nprivate and secure location.\n\nSharing your API key is strictly prohibited.\nThe API key is unique to each customer and application.\n\nPass the API key in the request header \&quot;x-api-key\&quot;.\n\nGiven below is an example of the curl command on how to pass the API key in the header:\n\n\n```\ncurl -X GET --header \&quot;Accept: application/json\&quot; --header \&quot;x-api-key: $api_key\&quot; \&quot;https://api.probe42.in/probe_lite/companies\&quot;\n\n```\n\n## Limits\n\nBe good. If you are sending too many requests too quickly, you will receive a 429 HTTP response.\nWe have rate-limiting set on our servers.\n\n## Errors\nThe following are the typical errors returned:\n\n403 - Forbidden when there&#39;s no api-key supplied, incorrect api-key or\n      an incorrect URL is given\n\n422 - Validation errors - for eg., given a wrong CIN format\n\n404 - when a resource is not found\n\n500 - any server side error\n\n503 - timeout errors - if we have some issue in our backend systems
    """
)


