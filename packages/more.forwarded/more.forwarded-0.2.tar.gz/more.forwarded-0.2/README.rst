more.forwarded: Forwarded header support for Morepath
=====================================================

If you want to run Morepath_ behind a trusted proxy that sets the
`Forwarded header`_, you can use ``more.forwarded`` to make Morepath
generate URLs that take this header into account.

**Note**: Only use this if you know you are behind a trusted proxy
that indeed sets the Forwarded header, otherwise you expose your
server to potential attacks.

.. _Morepath: http://morepath.readthedocs.org

.. _`Forwarded header`: http://tools.ietf.org/html/rfc7239
