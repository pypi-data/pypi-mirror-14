Nose-html-output plugin
=======================

A plugin for nosetests that will write out test results to results.html.

The code is adapted from the `example html output plugin`_ and the
`pyunit Html test runner`_.

This is an alternative ``nosehtmloutput`` (pypi name: ``nosehtmloutput-2``)
plugin that is not integrated to openstack.

How to use it
-------------

To enable the plugin in nose use the ``--with-html-output`` flag.

To specify the output file use ``--html-out-file`` or the environment
variable ``NOSE_HTML_OUT_FILE`` otherwise the output will be stored in
``results.html``.

Issues or improvement are welcome on the `github repo`_.


.. _`example html output plugin`: https://github.com/nose-devs/nose/blob/master/examples/html_plugin/htmlplug.py
.. _`pyunit Html test runner`: http://tungwaiyip.info/software/HTMLTestRunner.html
.. _`github repo`: https://github.com/cyraxjoe/nose-html-output
