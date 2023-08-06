A small command-line utility to take a CSV file and print a bar chart in
your terminal. Especially useful in combination with tools like CSVKit_,
q_, and jq_.

::

    $ curl -s http://www.census.gov/popest/data/national/totals/2015/files/NST-EST2015-alldata.csv | head -n 6 | bars --label NAME --value POPESTIMATE2015 --width 72 -
    NAME             POPESTIMATE2015
    United States        321,418,820 ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    Northeast Region      56,283,891 ▓░░░░░
    Midwest Region        67,907,403 ▓░░░░░░
    South Region         121,182,847 ▓░░░░░░░░░░░░
    West Region           76,044,679 ▓░░░░░░░
                                     +---------+---------------------------+
                                     0    100,000,000            400,000,000

* Repository: https://github.com/flother/bars
* Issues: https://github.com/flother/bars/issues

Installation
------------

::

    pip install -e git+https://github.com/flother/bars#egg=bars

Requirements
------------

* `Python 3`_
* `Click`_
* `Agate`_

Usage
-----

::

    Usage: bars [OPTIONS] CSV
    
      Load a CSV file and output a bar chart.
    
    Options:
      --label TEXT        Name or index of the column containing the label values.
                          Defaults to the first text column.
      --value TEXT        Name or index of the column containing the bar values.
                          Defaults to the first numeric column.
      --domain NUMBER...  Minimum and maximum values for the chart's x-axis.
      --width INTEGER     Width, in characters, to use to print the chart.
                          [default: 80]
      --skip INTEGER      Number of rows to skip.  [default: 0]
      --encoding TEXT     Character encoding of the CSV file.  [default: UTF-8]
      --no-header         Indicates the CSV file contains no header row.
      --printable         Only use printable characters to draw the bar chart.
      --help              Show this message and exit.


.. _CSVKit: http://csvkit.readthedocs.org/en/latest/
.. _q: http://harelba.github.io/q/
.. _jq: https://stedolan.github.io/jq/
.. _Python 3: https://docs.python.org/3/
.. _Click: http://click.pocoo.org/6/
.. _Agate: http://agate.readthedocs.org/en/1.3.1/
