encrypted-dict
==============
.. image:: https://travis-ci.org/grahamhar/encrypted-dict.svg?branch=master
       :target: https://travis-ci.org/grahamhar/encrypted-dict

Encrypt values in dict so that the dict remains readable in plain text except for the encrypted sections,
it's main use is for when outputing dicts to be stored on disk as yaml or json.

Setup
-----

pygpgme requires libgpgme11-dev on Ubuntu and on Mac OSX (via brew) you need gpgme and libgpg-error


Inspired by:

hiera-eyaml_ and hiera-eyaml-gpg_

.. _hiera-eyaml: https://github.com/TomPoulton/hiera-eyaml

.. _hiera-eyaml-gpg: https://github.com/sihil/hiera-eyaml-gpg
