from setuptools import setup


setup(
    name='update-plex',
    version='1.3.0',
    description='Tell your Plex TV library to update',
    author='George Hickman',
    author_email='george@ghickman.co.uk',
    url='https://github.com/ghickman/update_plex',
    license='MIT',
    entry_points={'console_scripts': ['update_plex=update_plex:run']},
    install_requires=['click', 'requests'],
    py_modules=['update_plex'],
)
