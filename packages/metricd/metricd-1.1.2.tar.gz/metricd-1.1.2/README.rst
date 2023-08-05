=============
metricd-agent
=============

.. image:: https://travis-ci.org/o/metric-agent.svg?branch=master
    :target: https://travis-ci.org/o/metric-agent

metricd is agent for collecting and sending metrics. Currently collects information about system and sends as JSON via HTTP. In the future more reporters (e.g statsd, graphite, riemann, influxdb) and collectors (e.g. metricd-nginx, metricd-haproxy, metricd-mysql, metricd-redis) will be available.

Installation
============

pip is easiest way to install metricd. 

**Dependencies**

* python 2.7, >=3.3 (tested with version 2.7, 3.3, 3.4, 3.5)
* Python development tools and libraries (called python-dev or devel)
* pip

**Installing dependencies**

Ubuntu / Debian::

    $ sudo apt-get install python-dev python-pip
    
RedHat / CentOS::

    $ sudo yum install python-pip python-devel gcc
    # You can find python-pip from EPEL repository

OSX

First of all, you need to install `Xcode <https://developer.apple.com/xcode/download/>`__

**Installing with pip**::

    $ sudo pip install metricd

**Upgrading**::

    $ sudo pip install metricd --upgrade

**Uninstalling**::

    $ sudo pip uninstall metricd

Running
=======

The following command prints metrics to console::

    metricd console
    
If you want to send metrics with HTTP POST as JSON::

    $ metricd http --url http://localhost:3000/collect
    
    ## with extra headers
    
    $ metricd http --url http://localhost:3000/collect --headers X-Foo=Bar --headers X-Access-Token=jaezei9G

License
=======

The MIT License (MIT)
Copyright (c) 2016 Osman Ungur

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
