Timeleft
========


Timeleft is a simple command line utility for displaying the amount of time left in a download. In the command line, one simply needs to input the file size remaining and the average download speed expected. Timeleft will output the time remaining in units that are easy to read.


Usage
-----


.. code-block:: bash

    $ timeleft 100MB 100MBps
    1.0 second
    $ timeleft 100MB 100mbps
    8.0 seconds
    $ timeleft 100MB 100mb/s
    8.0 seconds
    $ timeleft 100MB 1kbps
    9.0 days, 11.0 hours, 33.0 minutes, 20.0 seconds
    $ 3.4GB 3.4MBps
    17.0 minutes, 4.0 seconds
    $ timeleft 1.5YB 10gbps
    28561641.0 years, 172.0 days, 10.0 hours, 21.0 minutes, 39.25 seconds
    $ timeleft 100GB 100GBPS
    1.0 second

As shown in the examples above, Timeleft can take a variety of inputs to produce a human-readable output.
Arguments can be input in any order: the only requirement for arguments is that one has file size units and the other has download speed units.

Features
--------

- Both bits and bytes are supported as file and speed units are supported (don't let your ISP pull the wool over your eyes there). Accordingly, Timeleft is case-sensitive in that it distinguishes between B and b (i.e., 1MB = 8 Mb; all other characters *should* be case independent).

- Speed units can take the format of B/s or Bps (e.g., both 1MBps and 1MB/s are accepted).

- Sizes prefixes ranging from bits all the way up to yottabytes (2\ :sup:`80` bytes) are currently supported.

- The output format only shows the largest unit necessary to display the time remaining (i.e., "0.0 minutes, 23.0 seconds" will never occur).



Dependencies
------------

Timeleft is tested on Python 2.7 and 3.5 but should work on all versions 2.6 and above. There are no dependencies outside of the standard library. Testing (optionally included) is handled with Pytest.


Installation
------------


To install Timeleft, simply:

.. code-block:: bash

    $ pip install timeleft

Alternatively, if you would like to install from source:

.. code-block:: bash

    $ pip install git+https://github.com/swareham/timeleft.git




Pip will automatically add the "timeleft" executable to your path and you will be ready to go!


Credits
-------

- Logic for powering Timeleft: Sean Wareham
- Template for pip / setuptools support: Kenneth Reitz and all of the developers of requests at https://github.com/kennethreitz/requests