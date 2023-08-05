from distutils.core import setup

setup(
    name='amg',
    version='1.0.2',
    py_modules=['amg'],
    author='zewait',
    author_email='wait@h4fan.com',
    description='app manager tool',
    license='MIT',
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'amg = amg:main'
        ]
    }
)
