=======
gtrends
=======

gtrends is a Python library that eases the process of downloading Google Trend data. `Google Trends <http://www.google.com/trends>`_ is a service offered by Google which allows access to aggregate query volume data for specific search terms, over specific periods of time. This volume data is represented as a fraction of the total query volume on the given day or week.

Users with Google accounts can download these data into csv files, however there are several caveats which make the data difficult to process. The data only come in daily granularity up until 3 months worth of data, after which they become weekly. Even worse, Google normalizes the data, so that the largest percent query volume in the time series is set to an integer '100,' with all other values set to smaller integer values. This makes it difficult, for example, to collect several files and splice them together (such as to maintain a daily granularity via files of shorter time periods), since the data are on difference scales.

gtrends solves this by allowing developers to extract data with either weekly or daily granularity, with the same scaling throughout, without the need to worry over scaling and data manipulation themselves.

Usage
=====

gtrends only contains two functions, the primary one being ``collectTrends()``. It can be used by the following::

	import datetime
	import gtrends

	username = "myGoogleUsername"
	password = "myGooglePassword"

	terms = ["foo", "bar", "baz"]
	startDt = datetime.datetime(year=2015, month=1, day=1)
	endDt = datetime.datetime(year=2015, month=2, day=1)

	trends = gtrends.collectTrends(username, password, terms, startDt, endDt)


``collectTrends()`` returns a 2d list of the data, of format [datetime, val0, val1, val2, etc.], with an additional a header. For example, the above code snippet returns the list, ``trends``, as follows::

	date,foo,bar,baz
	1/1/2015,16.667,83.333,16.667
	1/2/2015,16.667,83.333,16.667
	1/3/2015,16.667,83.333,16.667
	1/4/2015,16.667,83.333,16.667
	1/5/2015,16.667,66.667,16.667
	1/6/2015,16.667,66.667,16.667
	1/7/2015,16.667,83.333,16.667
	1/8/2015,16.667,83.333,16.667
	1/9/2015,16.667,83.333,16.667
	1/10/2015,16.667,83.333,16.667

	...

	1/30/2015,16.667,83.333,16.667
	1/31/2015,16.667,100.00,16.667

The dates are of type datetime, and the numbers are floats rounded to 3 decimal places.
The data is normalized across the entire time period and between terms such that the largest value has a float of 100.0, and all other values are scaled accordingly.
Data is returned from [startDt, endDt), to the accuracy of the month (i.e. the specific day within the month does not matter).


Advanced Usage
==============
Granularity
-----------
With the optional argument ``granularity``, the granularity can be changed from the default of daily, to weekly. ``granularity`` takes a string of either ``'d'`` or ``'w'`` corresponding to daily or weekly, respectively.

Sum
---
``sum``, is an optional argument of type boolean. With this, the data of multiple terms can be summed together into one column. Default is ``False``.

SavePath
------------------
``savePath`` takes a string for a path to save the resultant csv. If left as the default ``None``, no file is saved.

Advanced Usage Example
----------------------
::

	import datetime
	import gtrends

	username = "myGoogleUsername"
	password = "myGooglePassword"

	terms = ["foo", "bar", "baz"]
	startDt = datetime.datetime(year=2015, month=1, day=1)
	endDt = datetime.datetime(year=2015, month=2, day=1)

	trends = gtrends.collectTrends(username, password, terms, startDt, endDt,
			granularity='w', sum=True, savePath="myDir/data.csv")

Note
====
The data is normalized at the end across all terms (if more than one), such that the largest value in the entire array is set to 100.0. Therefore, all term values are to scale between terms.

Raw Data
========
The secondary function ``collectRawTrends()`` allows you to collect the raw csv from Google Trends as a string::

	import datetime
	import gtrends
	
	username = "myGoogleUsername"
	password = "myGooglePassword"

	terms = ["foo", "bar", "baz"]
	startDt = datetime.datetime(year=2015, month=1, day=1)
	endDt = datetime.datetime(year=2015, month=2, day=1)

	trends = gtrends.collectRawTrends(username, password, terms, startDt, endDt,
			savePath="myDir/data.csv")

In this case, the granularity cannot be set: it is daily or weekly based on what Google naturally returns. The number of terms is limited to 5 (which is the max Google itself allows per csv file) and sumation is not supported (as in the optional argument ``sum`` in ``collectTrends()``). In addition, the regional data and related term data is included, rather than being discarded in ``collectTrends()``.

Installing
==========

Install via pip with::

	pip install gtrends

Requirements
============
This has so far only been tested on Python 2.7.

Issues
======
Please create an issue in the issue tracker.

License
=======
MIT License
	
	Copyright (c) 2015 Eric Salina

	Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Data Source: Google Trends (http://www.google.com/trends)
