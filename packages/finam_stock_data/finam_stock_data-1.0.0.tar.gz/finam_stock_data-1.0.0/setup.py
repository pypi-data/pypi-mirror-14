from distutils.core import setup

setup(
    name='finam_stock_data',
    version='1.0.0',
    author='Vladimir37',
    author_email='vladimir37work@gmail.com',
    url='https://github.com/Vladimir37/finam_stock_data/',
    description='Package for receiving historical stock data from Finam.',
    download_url='https://github.com/Vladimir37/finam_stock_data/archive/master.zip',
    license='MIT',
    install_requires=['pandas'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=['finam', 'stock', 'quotes', 'historical', 'finance', 'forex'],
    packages=['finam_stock_data'],
    package_data={
        'finam_stock_data': ['finam_stock_data'],
    },
    data_files=[('base', ['finam_stock_data/symbols.sqlite'])]
)
