Docutils Tiny HTML Writer
-------------------------
Docutils Tiny HTML Writer is another docutils html writer, with very light html
output. It will create mainly for use in other project's like doc generators or
web publishers, which want to use their own html headers and footers.

One of possible use:

.. code-block:: python
    :name: example

    from docutils.core import publish_string, publish_parts
    from docutils_tinyhtml import Writer
    from sys import version_info

    if version_info[0] < 3:
        from io import open

    writer = Writer()
    with open("README.rst", encoding="utf-8") as f:
        rst = f.read()

    # store full html output to html variable
    html = publish_string(source=rst,
                          writer=writer,
                          writer_name='html',
                          settings_overrides={'link': 'link', 'top': 'top'})

    # disable system message in html, no in stderr
    parts = publish_parts(source=rst,
                          writer=writer,
                          writer_name='html',
                          settings_overrides={'no_system_messages': True})

    # store only html body
    body = parts['html_title'] + parts['body'] + parts['html_line'] + \
        parts['html_footnotes'] + parts['html_citations'] + \
        parts['html_hyperlinks']


Or you can use rst2html-tiny command tool like standard rst2html:

.. code-block:: sh

    ~$ rst2html-tiny README.rst > README.html       # generate html from reStructured text
    ~$ rst2html-tiny -h                             # help output


Installation
------------
.. code-block:: sh

    ~$ pip install docutils-tinyhtmlwriter
