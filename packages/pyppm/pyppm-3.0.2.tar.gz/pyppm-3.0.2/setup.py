from setuptools import setup, find_packages

install_requires = ['pycrypto']

setup(
    name="pyppm",
    url="https://github.com/her0e1c1/pwm",
    version="3.0.2",
    description="python password manager",
    author="Hiroyuki Ishii",
    author_email="hiroyuki.ishii.42@gmail.com",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points="""
    [console_scripts]
    pyppm = pyppm.main:main
    """
)
