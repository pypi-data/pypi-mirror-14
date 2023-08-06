etcd v3 API
------------

This package contains a script for generating etcd APIv3 bindings.
If you are only interested in getting bindings for published etcd version,
just use pip to get a version that matches your etcd from PyPI.

If you want to generate bindings yourself, you should:

* Clone this package
* Checkout the gogoproto/protobuf and etcd submodules with desired versions
* Optionally edit the ``version/version.go`` file in etcd submodule, so the
  ``Version`` variable is set to preferred value.
* Run the ``./make.py`` script. This would generate ``setup.py``, ``MANIFEST``
  and the api files compiled to python.
* Create the distribution or do the install using the generated ``setup.py``
