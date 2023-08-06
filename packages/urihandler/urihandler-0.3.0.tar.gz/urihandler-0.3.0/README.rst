UriHandler
==========

.. image:: https://badge.fury.io/py/urihandler.png
        :target: http://badge.fury.io/py/urihandler

.. image:: https://travis-ci.org/OnroerendErfgoed/urihandler.png?branch=master
        :target: https://travis-ci.org/OnroerendErfgoed/urihandler
.. image:: https://coveralls.io/repos/OnroerendErfgoed/urihandler/badge.png?branch=master
        :target: https://coveralls.io/r/OnroerendErfgoed/urihandler

This very simple application is meant to be the handler on a domain that
handles Cool Uri's (http://www.w3.org/TR/cooluris/) with 303 redirects.

All it does is map Uri's to other uri's and redirect them. To make thing easy
you can either redirect by hitting the full URI (eg.
`http://id.example.com/foo/15`) or by querying a handle service (eg.
`http://id.example.com/handle?uri=http://id.example.com/foo/15`). Both of these
will redirect you. The handle service also works for non-http URI's. Finally,
there's a service that just returns information without performing a redirect,
eg. `http://id.example.com/uris?uri=http://id.example.com/foo/15`. This can be
handy to bypass some of the strangeness that happens when you combine Cool uri's
with CORS and custom HTTP headers.

Configuration is done by editing a YAML file. For each URI you need to register
a regex and a redirect template. The regex should use named placeholders, as
well as the redirect string. An optional argument `mount` determines if your
`match` is living at the server root or is absolute (eg. because it's a URN). Not
setting `mount` sets it to `True`.
