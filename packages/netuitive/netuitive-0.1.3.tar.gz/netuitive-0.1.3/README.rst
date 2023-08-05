===============================
Netuitive Python Client
===============================

|BuildStatus|_

.. |BuildStatus| image:: https://travis-ci.org/Netuitive/netuitive-client-python.svg?branch=master
.. _BuildStatus: https://travis-ci.org/Netuitive/netuitive-client-python
.. image:: https://coveralls.io/repos/github/Netuitive/netuitive-client-python/badge.svg?branch=master :target: https://coveralls.io/github/Netuitive/netuitive-client-python?branch=master

What is Netuitive monitoring?
-----------------------------
Netuitive provides an adaptive monitoring and analytics platform for cloud infrastructure and web applications.
Netuitive learns behaviors and utilizes pre-set dynamic policies that reduce the manual effort and human-guesswork typically required to monitor systems and applications.
This unique technology enables IT operations and developers to automate performance analysis, detect relevant anomalies, and determine efficient capacity utilization.

Features
--------

* Create a Netuitive Element with the following data:
    * Element Name
    * Attributes
    * Tags
    * Metric Samples
    * Element relations
    * Location
    * Metric Tags

* Create a Netuitive Event with the following data
    * Element Name
    * Event Type
    * Title
    * Message
    * Level
    * Tags
    * Source


Usage
-----

###### Setup the Client

``ApiClient = netuitive.Client(api_key='<my_api_key>')``


###### Setup the Element

``MyElement = netuitive.Element()``

###### Add an Attribute

``MyElement.add_attribute('Language', 'Python')``

###### Add an Element relation

``MyElement.add_relation('my_child_element')``

###### Add a Tag

``MyElement.add_tag('Production', 'True')``

###### Add a Metric Sample

``MyElement.add_sample('cpu.idle', 1432832135, 1, host='my_hostname')``

###### Add a Metric Sample with a Sparse Data Strategy

``MyElement.add_sample('app.zero', 1432832135, 1, host='my_hostname', sparseDataStrategy='ReplaceWithZero')``

###### Add a Metric Sample with unit type

``MyElement.add_sample('app.requests', 1432832135, 1, host='my_hostname', unit='requests/s')``

###### Add a Metric Sample with utilization tag

``MyElement.add_sample('app.requests', 1432832135, 1, host='my_hostname', tags=[{'utilization': 'true'}])``

###### Add a Metric Sample with min/max values

``MyElement.add_sample('app.percent_used', 1432832135, 50, host='my_hostname', unit='percent', min=0, max=100)``

###### Send the Samples

``ApiClient.post(MyElement)``

###### Remove the samples already sent

``MyElement.clear_samples()``


###### Create an Event

``MyEvent = netuitive.Event(hst, 'INFO', 'test event','big old test message', 'INFO')``

###### Send the Event

``ApiClient.post_event(MyEvent)``

###### Check that our local time is set correctly (returns True/False)

``ApiClient.time_insync()``

Example
-------


    import netuitive

    ApiClient = netuitive.Client(api_key='aaaa9956110211e594444697f922ec7b')

    MyElement = netuitive.Element()

    MyElement.add_attribute('Language', 'Python')
    MyElement.add_attribute('app_version', '7.0')

    MyElement.add_relation('my_child_element')

    MyElement.add_tag('Production', 'True')
    MyElement.add_tag('app_tier', 'True')

    MyElement.add_sample('app.error', 1432832135, 1, host='appserver01')
    MyElement.add_sample('app.request', 1432832135, 10, host='appserver01')

    ApiClient.post(MyElement)

    MyElement.clear_samples()

    MyEvent = netuitive.Event('appserver01', 'INFO', 'test event','big old test message', 'INFO')

    ApiClient.post_event(MyEvent)

    if ApiClient.time_insync():
        print('we have time sync with the server')

Copyright and License
---------------------

Copyright 2015-2016 Netuitive, Inc. under [the Apache 2.0 license](LICENSE).
