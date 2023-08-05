from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="pyppm",
    url="https://github.com/her0e1c1/pwm",
    version="3.0.0",
    description="python password manager",
    author="Hiroyuki Ishii",
    author_email="hiroyuki.ishii.42@gmail.com",
    packages=find_packages(),
    install_requires=required,
    entry_points="""
    [console_scripts]
    pyppm = pyppm.main:main
    """
)
