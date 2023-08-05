
==========
 Skyfield
==========

.. rst-class:: motto

   *Elegant Astronomy for Python*

.. testsetup::

   __import__('skyfield.tests.fixes').tests.fixes.setup()

   import os
   os.chdir('../..')  # same directory as de430t.bsp, hopefully

.. testcode::

    from skyfield.api import load

    planets = load('de421.bsp')
    earth, mars = planets['earth'], planets['mars']

    ts = load.timescale()
    t = ts.now()
    position = earth.at(t).observe(mars)
    ra, dec, distance = position.radec()

    print(ra)
    print(dec)
    print(distance)

.. testoutput::

    10h 47m 56.24s
    +09deg 03' 23.1"
    2.33251 au

Skyfield is a pure-Python astronomy package
that makes it easy to generate high precision research-grade
positions for planets and Earth satellites.
You can compute either geocentric coordinates
as shown in the example above,
or topocentric coordinates specific to your location
on the Earth’s surface:

.. testcode::

    boston = earth.topos('42.3583 N', '71.0636 W')
    position = boston.at(t).observe(mars)
    alt, az, d = position.apparent().altaz()

    print(alt)
    print(az)

.. testoutput::

    25deg 27' 54.0"
    101deg 33' 44.0"

The official documentation is available through the links
in the Table of Contents below.
You can also visit:

* `Skyfield on the Python Package Index <https://pypi.python.org/pypi/skyfield>`_

* `GitHub project page <https://github.com/brandon-rhodes/python-skyfield/>`_

* `GitHub issue tracker <https://github.com/brandon-rhodes/python-skyfield/issues>`_

News
====

**2016 March 24**
  With the release of Skyfield 0.7,
  the final API upheavals of the pre-1.0 era are now complete.
  The introduction of the new timescale object
  has now eliminated all hidden state from the library,
  and has cleared the way for rapid development going forward.

  Unless users encounter significant problems,
  version 1.0 should follow as soon as the documentation —
  and in particular the API Reference —
  has received a bit more polish.
  The project is almost there!

Table of Contents
=================

.. toctree::
   :maxdepth: 2

   installation
   positions
   time
   planets
   stars
   earth-satellites
   api
   design

.. testcleanup::

   __import__('skyfield.tests.fixes').tests.fixes.teardown()
