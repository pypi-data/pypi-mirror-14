RIPE Atlas Cousteau
===================

|Documentation| |Build Status| |Code Health| |PYPI Version| |Python Versions| |Python Implementations| |Python Format|

A python wrapper around RIPE ATLAS API.

(Until version 0.9.* this wrapper supported v1 API. After version 0.10 and above v2 RIPE ATLAS API is only supported.)

Installation
------------

You can install by either cloning the repo and run the following inside
the repo:

.. code:: bash

    $ python setup.py install

or via pip using:

.. code:: bash

    $ pip install ripe.atlas.cousteau

Usage
-----

Creating a Measurement
~~~~~~~~~~~~~~~~~~~~~~

Creating two new RIPE Atlas UDMs is as easy as:

.. code:: python

    from datetime import datetime
    from ripe.atlas.cousteau import (
      Ping,
      Traceroute,
      AtlasSource,
      AtlasCreateRequest
    )

    ATLAS_API_KEY = ""

    ping = Ping(af=4, target="www.google.gr", description="testing new wrapper")

    traceroute = Traceroute(
        af=4,
        target="www.ripe.net",
        description="testing",
        protocol="ICMP",
    )

    source = AtlasSource(type="area", value="WW", requested=5)

    atlas_request = AtlasCreateRequest(
        start_time=datetime.utcnow(),
        key=ATLAS_API_KEY,
        measurements=[ping, traceroute],
        sources=[source],
        is_oneoff=True
    )

    (is_success, response) = atlas_request.create()

Keep in mind that this library is trying to comply with what is stated
in the `documentation pages`_. This means that if you try to create a
request that is missing a field stated as required, the library won't go
ahead and do the HTTP query. On the contrary, it will raise an exception
with some info in it.
The available measurements types are Ping, Traceroute, Dns, Sslcert, Ntp, Http.

.. _documentation pages: https://atlas.ripe.net/docs/measurement-creation-api/

Changing Measurement Sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similarly if you want to change (add in the following example) probes
for an existing measurement you can do:

.. code:: python

    from ripe.atlas.cousteau import AtlasChangeSource, AtlasChangeRequest

    ATLAS_MODIFY_API_KEY = ""

    source = AtlasChangeSource(
        value="GR",
        requested=3,
        type="country",
        action="add"
    )

    atlas_request = AtlasChangeRequest(
        key=ATLAS_MODIFY_API_KEY,
        msm_id=1000001,
        sources=[source]
    )

    (is_success, response) = atlas_request.create()

Same applies if you want to remove probes, you just have to
change "action" key to "remove" and specify probes you want to remove.
Keep in mind remove action supports only a list of probes and not the rest of the source types.
For more info check the appropriate `docs`_.

.. _docs: https://atlas.ripe.net/docs/rest/#participation-request

Stopping Measurement
~~~~~~~~~~~~~~~~~~~~

You can stop a measurement with:

.. code:: python

    from ripe.atlas.cousteau import AtlasStopRequest

    ATLAS_STOP_API_KEY = ""

    atlas_request = AtlasStopRequest(msm_id=1000001, key=ATLAS_STOP_API_KEY)

    (is_success, response) = atlas_request.create()

In order to be able to successfully create most of the above you need to
create an `API key`_.

.. _API key: https://atlas.ripe.net/docs/keys/

Make Any API Get Requests
~~~~~~~~~~~~~~~~~~~~~~~~~

If you know the url path you can make any request easily towards ATLAS
API.

.. code:: python

    url_path = "/api/v2/anchors"
    request = AtlasRequest(**{"url_path": url_path})
    result = namedtuple('Result', 'success response')
    (is_success, response) = request.get()
    if not is_success:
        return False

    return result.response["participant_count"]

Fetch Results
~~~~~~~~~~~~~

You can fetch results for any measurements using cousteau. In the
following example we are getting all results for measurement ID 2016892
and for probe IDs 1,2,3,4 between 2015-05-19 and 2015-05-20. Times can
be python datetime objects, Unix timestamps or string representations of
dates.

.. code:: python

    from datetime import datetime
    from ripe.atlas.cousteau import AtlasResultsRequest

    kwargs = {
        "msm_id": 2016892,
        "start": datetime(2015, 05, 19),
        "stop": datetime(2015, 05, 20),
        "probe_ids": [1,2,3,4]
    }

    is_success, results = AtlasResultsRequest(**kwargs).create()

    if is_success:
        print(results)

Fetch real time results
~~~~~~~~~~~~~~~~~~~~~~~

Besides fetching results from main API it is possible to get results
though `streaming API`_.

.. code:: python

    from ripe.atlas.cousteau import AtlasStream

    def on_result_response(*args):
        """
        Function that will be called every time we receive a new result.
        Args is a tuple, so you should use args[0] to access the real message.
        """
        print args[0]

    atlas_stream = AtlasStream()
    atlas_stream.connect()
    # Measurement results
    channel = "result"
    # Bind function we want to run with every result message received
    atlas_stream.bind_channel(channel, on_result_response)
    # Subscribe to new stream for 1001 measurement results
    stream_parameters = {"msm": 1001}
    atlas_stream.start_stream(stream_type="result", **stream_parameters)

    # Probe's connection status results
    channel = "probe"
    atlas_stream.bind_channel(channel, on_result_response)
    stream_parameters = {"enrichProbes": True}
    atlas_stream.start_stream(stream_type="probestatus", **stream_parameters)

    # Timeout all subscriptions after 5 secs. Leave seconds empty for no timeout.
    # Make sure you have this line after you start *all* your streams
    atlas_stream.timeout(seconds=5)
    # Shut down everything
    atlas_stream.disconnect()

The available stream parameters for every stream type are described in
the `streaming results docs`_

.. _streaming API: https://atlas.ripe.net/docs/result-streaming/
.. _streaming results docs: https://atlas.ripe.net/docs/result-streaming/

Filter Probes/Measurements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This feature queries API for probes/measurements based on specified filters. Filters 
should be as specified in `filter_api`_. It hides all the complexity of traversing
the API using the next url each time there are more objects. It returns
a python generator that you can use to access each object.

Fetches all probes from NL with asn\_v4 3333 and with tag NAT

.. code:: python

    from ripe.atlas.cousteau import ProbeRequest

    filters = {"tags": "NAT", "country_code": "NL", "asn_v4": "3333"}
    probes = ProbeRequest(**filters)

    for probe in probes:
        print(probe["id"])

    # Print total count of found probes
    print(probes.total_count)

Fetches all specified measurements.

.. code:: python

    from ripe.atlas.cousteau import MeasurementRequest

    filters = {"status": 1}
    measurements = MeasurementRequest(**filters)

    for msm in measurements:
        print(msm["msm_id"])

    # Print total count of found measurements
    print(measurements.total_count)

.. _filter_api: https://atlas.ripe.net/docs/rest/

Represent Probes/Measurements Meta data in python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This will allow you to have a python object with attributes populated from probes/measurements meta data.
Every time you create a new instance it will fetch meta data from API and return an object with selected attributes.

.. code:: python

    from ripe.atlas.cousteau import Probe, Measurement

    probe = Probe(id=3)
    print(probe.country_code)
    print(probe.is_anchor)
    print(probe.is_public)
    print(probe.address_v4)
    print(dir(probe)) # Full list of properties

    measurement = Measurement(id=1000002)
    print(measurement.protocol)
    print(measurement.description)
    print(measurement.is_oneoff)
    print(measurement.is_public)
    print(measurement.target_ip)
    print(measurement.target_asn)
    print(measurement.type)
    print(measurement.interval)
    print(dir(measurement)) # Full list of properties

Colophon
========

But why `Cousteau`_? The RIPE Atlas team decided to name all of its
modules after explorers, and this is not an exception :)

.. _Cousteau: http://en.wikipedia.org/wiki/Jacques_Cousteau
.. |Build Status| image:: https://travis-ci.org/RIPE-NCC/ripe-atlas-cousteau.png?branch=master
   :target: https://travis-ci.org/RIPE-NCC/ripe-atlas-cousteau
.. |Code Health| image:: https://landscape.io/github/RIPE-NCC/ripe-atlas-cousteau/master/landscape.png
   :target: https://landscape.io/github/RIPE-NCC/ripe-atlas-cousteau/master
.. |PYPI Version| image:: https://img.shields.io/pypi/v/ripe.atlas.cousteau.svg
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/ripe.atlas.cousteau.svg
.. |Python Implementations| image:: https://img.shields.io/pypi/implementation/ripe.atlas.cousteau.svg
.. |Python Format| image:: https://img.shields.io/pypi/format/ripe.atlas.cousteau.svg
.. |Documentation| image:: https://readthedocs.org/projects/ripe-atlas-cousteau/badge/?version=latest
   :target: https://ripe-atlas-cousteau.readthedocs.org/en/latest/?badge=latest



Releases History
================
1.2 (released 2016-03-02)
-------------------------
Changes:
~~~~~~~~
- Backwards incompatible field changes on the Measurement object:

 - destination_address -> target_ip
 - destination_asn -> target_asn
 - destination_name -> target

1.1 (released 2016-02-09)
-------------------------
New features:
~~~~~~~~~~~~~
- Start supporting Anchors listing API.
- Brand new documentation hosted on readthedocs.

Changes:
~~~~~~~~
- Various refactorings to clean up codebase.

1.0.7 (released 2016-01-13)
---------------------------
Changes:
~~~~~~~~
- Backwards compatible change of the format we expect for measurement type to handle upcoming change in the API.

Bug Fixes:
~~~~~~~~~~
- Fix bug when creating stream for probes connection channel. Updating also wrong documentation.

1.0.6 (released 2015-12-15)
---------------------------
Changes:
~~~~~~~~
- Add copyright text everywhere for debian packaging.

1.0.5 (released 2015-12-14)
---------------------------
Changes:
~~~~~~~~
- Add tests to the package itself.
- Make user-agent changeable by the user.
- Various refactorings.

1.0.4 (released 2015-11-06)
---------------------------
Changes:
~~~~~~~~
- Handle both string/dictionary as input for probe_ids filter for Result and LatestResult requests.

1.0.2 (released 2015-10-26)
---------------------------
Bug Fixes:
~~~~~~~~~~
- Fix bug where key parameter was added to the url even if it was empty.
- Fix bug where we didn't try to unjson 4xx responses even if they could contain json structure.

1.0.1 (released 2015-10-23)
---------------------------
Changes:
~~~~~~~~
- Now we conform to new API feature that allows for specifying tags when adding probes to existing measurements

Bug Fixes:
~~~~~~~~~~
- Fix bug we didn't allow user to specify single tag include/exclude.

1.0 (released 2015-10-21)
-------------------------
New features:
~~~~~~~~~~~~~
- Add support for include/exclude tags in changing sources requests.
- Add support for latest results API call.
- Implement HTTP measurement creation.
- Support for python 3 (<=3.4).
- Support for pypy/pypy3.
- Support for wheels format.

Changes:
~~~~~~~~
- Migrate all Atlas requests to use requests library and refactor a lot of code to have a cleaner version.
- Create an API v2 translator to address several option name changing. A deprecation warning will be given.

Bug Fixes:
~~~~~~~~~~
- Fix bug where python representation of measurements without a stop time was exploding. 
- Make sure start/stop timestamps in measurement create request are always in UTC.

0.10.1 (released 2015-10-06)
----------------------------
New features:
~~~~~~~~~~~~~
- Implement support for object return in the request generators for probe/measurement.

Changes:
~~~~~~~~
- Probe/Measurement python representation takes meta data from v2 API as well. Now everything should point to v2 API.

0.10 (released 2015-10-01)
--------------------------
New features:
~~~~~~~~~~~~~
- add object representation of meta data for a probe or a measurement.

Changes:
~~~~~~~~
- Abandon v1 RIPE ATLAS API and use only v2.

Bug Fixes:
~~~~~~~~~~
- Fix bug that prevented users from specifying all possible source types when they tried to add more probes to existing measurements.
- Cover case where a user specified really long list of probes/measurements in the ProbeRequest/MeasurementRequest that was causing 'HTTP ERROR 414: Request-URI Too Long'. Additionally, now if API returns error raise an exception instead of stopping iteration.

0.9.2 (released 2015-09-21)
---------------------------
Changes:
~~~~~~~~
- Small refactor of Stream class and manually enforce websockets in SocketIO client

0.9.1 (released 2015-09-03)
---------------------------
Bug Fixes:
~~~~~~~~~~
- Fix bug related to binding result atlas stream.

0.9 (released 2015-09-01)
-------------------------
New features:
~~~~~~~~~~~~~
- add support for fetching real time results using RIPE Atlas stream server.
- this version and on will be available on PYPI.

0.8 (released 2015-08-31)
-------------------------
New features:
~~~~~~~~~~~~~
- add support for NTP measurements.

0.7 (released 2015-06-03)
-------------------------
New features:
~~~~~~~~~~~~~
- add support for fetching probes/measurements meta data using python generators.

0.6 (released 2014-06-17)
-------------------------
New features:
~~~~~~~~~~~~~
- add support for querying results based on start/end time, msm_id and probe id.

Changes:
~~~~~~~~
- add http agent according to package version to all requests.

0.5 (released 2014-05-22)
-------------------------
Changes:
~~~~~~~~
- change package structure to comply with the new structure of atlas packages
- add continuous integration support

 - add tests
 - enable travis
 - enable code health checks

- add required files for uploading to github

0.4 (released 2014-03-31)
-------------------------
New features:
~~~~~~~~~~~~~
- add support for stopping a measurement.

0.3 (released 2014-02-25)
-------------------------
New features:
~~~~~~~~~~~~~
- add simple support for HTTP GET queries.

0.2 (released 2014-02-03)
-------------------------
New features:
~~~~~~~~~~~~~
- add support for adding/removing probes API request.

Changes:
~~~~~~~~
- use AtlasCreateRequest instead of AtlasRequest for creating a new measurement.

0.1 (released 2014-01-21)
-------------------------
- Initial release.


