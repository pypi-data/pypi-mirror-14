import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('new_html/new_html.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "new_html",
    packages = ["new_html"],
    entry_points = {
        "console_scripts": ['html = new_html.new_html:new_html']
        },
    version = version,
    description = "Python command line html creator",
    long_description = long_descr,
    author = "Oscar Vazquez",
    author_email = "oscar.vazquez2012@gmail.com",
    url = "https://github.com/oscarvazquez/command_line_tool_demo"
)