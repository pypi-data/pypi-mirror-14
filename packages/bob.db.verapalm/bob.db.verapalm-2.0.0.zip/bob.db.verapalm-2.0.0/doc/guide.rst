.. vim: set fileencoding=utf-8 :
.. @author: Pedro Tome <Pedro.Tome@idiap.ch>
.. @date:   Wed Jan  14 12:28:25 CET 2015

==============
 User's Guide
==============

This package contains the access API and descriptions for the `VERA Palmvein <https://www.idiap.ch/dataset/vera-palmvein>`_ and the `VERA Spoofing Palmvein <https://www.idiap.ch/dataset/vera-spoofingpalmvein>`_ database.
It only contains the Bob_ accessor methods to use the DB directly from python, with our certified protocols.
The actual raw data for the `VERA Palmvein <https://www.idiap.ch/dataset/vera-palmvein>`_ and the `VERA Spoofing Palmvein <https://www.idiap.ch/dataset/vera-spoofingpalmvein>`_ database should be downloaded from the original URL.


The Database Interface
----------------------

The :py:class:`bob.db.verapalm.Database` complies with the standard biometric verification database as described in :ref:`commons`, implementing both interfaces :py:class:`bob.db.verification.utils.SQLiteDatabase` and :py:class:`bob.db.verification.utils.ZTDatabase`.

.. todo::
   Explain the particularities of the :py:class:`bob.db.verapalm.Database`.


.. _bob: https://www.idiap.ch/software/bob
