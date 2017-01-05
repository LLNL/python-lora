# Python LORA Interface

Maintainer: Ian Lee <ian@llnl.gov>

This package is an attempt to create a Python interface to the LC Lorenz REST API: LORA

The LORA API is documented, with examples, at: https://lc.llnl.gov/lorenz/lora/

## Usage

Very much a work in progress, but here is a rough idea of how you could use this in an interactive Python terminal:

```
>>> import lora

>>> cz_lora = lora.LoraSession()
>>> cz_lora.login()
Pin & Token: xxxxxxxx

>>> cz_lora.getAllClusters()
{
    'error': '',
    'output': {
        'accounts': [
            'ansel',
            'aztec',
            'cab',
            'catalyst',
            'herd',
            'oslic',
            'quartz',
            'surface',
            'syrah',
            'vulcan'
        ]
    },
    'status': 'OK'
}
```

## Getting Started

### Developer

To get started:

    # Set up the environment
    $ python -m virtualenv venv
    $ source venv/bin/activate

    # Install the dependencies
    $ pip install -r requirements.txt

    # Test that everything is working
    $ python test.py

## Contributing

Contributions to this package are very welcome! Please feel free to fork the repository, add new functionality, and submit a pull request!

If you have any questions, please [open a ticket](https://github.com/llnl/python-lora/issues).

## Future Ideas / Work

* The Python Requests ecosystem includes a package, [requests-kerberos](https://github.com/requests/requests-kerberos) that can provide authentication support for Kerberos / GSSAPI. This might be a better way to interact with with the LC environment, particular for applications running *on* the actual systems.
