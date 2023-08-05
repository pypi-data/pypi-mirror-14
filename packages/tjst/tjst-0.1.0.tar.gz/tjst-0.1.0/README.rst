tjst
====


Description
-----------

tjst = Tiny JavaScript Templating

High performance JS template engine.

It supports:

  - Anything you can write on JS =)
  - Server-side and client-side compilation.
  - ...?

It not supports:

  - Templates inheritence.
  - Includes.
  - ...?


Installation
------------
::

    $ git clone https://bitbucket.org/dkuryakin/tjst.git
    $ cd tjst && python setup.py install

or

::

    $ pip install tjst


Quickstart
----------

tjst supports only <% %> and <%= %> tags.

Suppose, we have file **index.html** file in some folder:

.. code-block:: html

    <!doctype html>
    <html>
        <head>
            <script src="tpl.js"></script>
        </head>
        <body>
            <div id="content"></div>

            <script>
                var context = {
                    users: [
                        {name: "Jeff", online: true,   info: "Jeff likes html"},
                        {name: "Mike", online: true,   info: "Mike likes css"},
                        {name: "Rose", online: false,  info: "Rose likes javascript"},
                        {name: "Anna", online: false,  info: "Anna likes perl"},
                    ]
                };
                document.getElementById('content').innerHTML = templates['tpl.html'](context);
            </script>
        </body>
    </html>


And template file **tpl.html** in the same folder:

.. code-block::

    <% for (var i = 0; i < users.length; i++) { %>
        <div>
            <strong style="color: <%=users[i].online ? 'green' : 'red'%>"><%=users[i].name%></strong> - <%=users[i].info%>
        </div>
    <% } %>


Install tjst and go to this folder. Compile template:

::

    $ tjst-compile tpl.html tpl.js


Now view **index.html** in your browser. You can find all examples here: https://bitbucket.org/dkuryakin/tjst/src/HEAD/tjst/examples/


Use as command-line tool
------------------------

::

    $ tjst-compile -e html,my-tpl-extension /path/to/template/file.html/or/folder /path/to/compiled/file.js


Use in python code
------------------

.. code-block:: python

    from tjst import compile_text2text, compile_file2file
    js = compile_text2text('''
    <div>
    <% for (var i = 0; i < 10; i++) { %>
        <p><%=i%></p>
    <% } %>
    ''')
    compile_file2file('templates_file_or_dir_path', 'dst_path.js', ['html', 'txt', 'my-ext'])


Tests
-----

You can run tests with following commands:

::

    $ git clone https://bitbucket.org/dkuryakin/tjst.git
    $ cd tjst && python setup.py test


Changelog
---------

v0.1.0
 - Basic functionality. Py3 support was not tested.