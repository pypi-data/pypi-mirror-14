This provides a Python wrapper around Viddler's v2 API.

**Changes in version 0.5**

* Provides better support for Viddler's update to TLS 1.2 and SNI

If you are getting ``Connection Reset by Peer`` messages, you probably need to install pyOpenSSL: see `http://urllib3.readthedocs.org/en/latest/security.html#openssl-pyopenssl`_

``pyviddler`` checks for this package and does the injection for you.

