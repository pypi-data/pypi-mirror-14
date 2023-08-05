# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "probe-py"
VERSION = "1.1.0"



# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.10", "six >= 1.9", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Probe Lite",
    author_email="",
    url="",
    keywords=["Swagger", "Probe Lite"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Probe provides you access to information on all companies in India. Data collected, cleaned and curated from multiple sources is made available through our APIs now.\n\n\n Come experience and build something awesome!\n\n\n\n All endpoints are accessible only via https and are located at `api.probe42.in`\n\n\n ## Authentication\n\n In order to make calls to our API, you will to include your API key in the request header\n as given in the example below.\n\n Write to us at [apiteam@probe42.in](mailto:apiteam@probe42.in) to create a developer account.\n\n It is very important to keep your API key as a secret and store it in a\n private and secure location. Sharing your API key is strictly prohibited.\n The API key is unique to each customer and application.\n\n Pass the API key in the request header \&quot;x-api-key\&quot;.\n\n Given below is an example of the curl command on how to pass the API key\n and the API version in the header:\n\n\n ```\n curl -X GET --header \&quot;Accept: application/json\&quot;\n    --header \&quot;x-api-key: $api_key\&quot;\n    --header \&quot;x-api-version 1.1\&quot;\n   \&quot;api.probe42.in/probe_lite/companies\&quot;\n\n ```\n\n *You must replace $api_key in the above with your API key.*\n\n ## Limits\n\n Be good. If you are sending too many requests too quickly, you will receive a 429 HTTP response.\n We have rate-limiting set on our servers.\n\n ## Errors\n The following are the typical errors returned:\n\n 403 - Forbidden when there&#39;s no api-key supplied, incorrect api-key or\n       an incorrect URL is given\n\n 422 - Validation errors - for eg., given a wrong CIN format\n\n 404 - when a resource is not found\n\n 500 - any server side error\n\n 502 - timeout errors - if we have some issue in our backend systems
    """
)


