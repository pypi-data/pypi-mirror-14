from setuptools import setup, find_packages

setup(
    name='HookWorker',
    version='0.0.5',
    packages=find_packages(exclude=("./tests", "__pycache__")),
    url='https://github.com/Capitains/Hook-Worker',
    license='GNU GPL',
    author='Thibault Clerice',
    author_email='leponteineptique@gmail.com',
    description='Lightweight API to handle call and distribute them over a redis server',
    install_requires=[
        "HookTest==0.0.6",
        "Flask==0.10.1",
        "rq==0.5.5",
        "redis>=2.7.0",
        "tornado==4.2.1"
    ],
    entry_points={
        'console_scripts': ['hookworker-api=HookWorker.cmd:cmd'],
    }
)
