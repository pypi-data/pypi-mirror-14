nwid
####
A terminal widgets framework for humans.
===========================================================
.. image:: https://www.quantifiedcode.com/api/v1/project/d817599b176740e49b42d1f8402d4d3e/badge.svg
  :target: https://www.quantifiedcode.com/app/project/d817599b176740e49b42d1f8402d4d3e
  :alt: Code issues
----

Please note that this is a work in progress. The API will likely change many
times before it becomes stable. Use at your own risk.

Nwid is a terminal widgets framework for humans.

It is designed to be an easy-to-use, light-weight (no dependencies), terminal
widget library and application framework for building terminal GUIs. It has
intuitive widgets, a simple and recognizable event loop, and a container
``App`` that can be extended or used as-is. Its design and components take some
inspiration from the well-known web browser DOM as well as the python packages
`urwid <http://urwid.org/>`_ and
`npyscreen <http://npyscreen.readthedocs.org/index.html>`_.

Although there already are a handful of terminal user-interface libraries in
python, I have found them to be either cumbersome to use or difficult to extend
because of their design. The python curses module is itself unweildly and
desperately needs a layer of abstraction to hide its unique details and oddly
named functions. Nwid aims to be this intuitive, easy to extend abstraction
layer. The nwid philosophy is to let you create and describe the widgets with
intuitive attributes and methods, and the framework will take care of the
cumbersome terminal details. The code is pythonic and easy to read, which makes
it easy to extend.

A low-level knowledge of terminals and tty is not necessary to using this
framework. To get started, check out the examples in the examples directory.
Nwid is designed to be conceptually easy to understand, and the examples are
intended to exhibit the basic concepts in order to give a helpful overview of
the capabilities and structure of the framework. After looking at the examples,
you can read `Modules and Components`_ for more specific details about the
framework.

If you have any questions, comments, or suggestions I'd love to hear them:
harold (a) bradleystudio.net


Installing and including in projects
====================================

Installing nwid
---------------

.. code:: bash

    $ git clone git@github.com:hbradleyiii/nwid.git
    $ cd <project directory>
    $ pip install -e .

Running Tests
-------------

.. code:: bash

    $ cd <project directory>
    $ py.test

Importing and Basic Usage
-------------------------

.. code:: python

    >>> import nwid

    >>> app = nwid.App()
    >>> app.window.add( {
            nwid.Title : { 'text' : 'An nwid App!' },
            nwid.LabeledTextBox : {
                'text' : 'Your input:',
                'validator' : App.validate_function,
                'name' :
                }
            nwid.Button : {
                'text' : 'Click me!',
                'click' : App.callback_function,
                }
            })

    >>> app.run()


Modules and Components
======================

Overview
--------

The nwid framework is made of three major components, the ``App`` class for
managing windows and running the event loop, the ``Window`` class for
containing and managing widgets, and the widget module for creating the user
interactive widgets (such as, textfields, labels, and dropdown boxes).

The ``App`` is the base controller for the application. Besides controling the
event loop, it is responsible for initializing the curses environment and
handling the screen object. This class can be used as-is or may be extended by
a custom class with application-specific controller methods. The ``App`` class
has a special property, the ``App.window_stack``, that keeps track of the
current window and any open window that has not yet been closed but is covered
up (partly or completely) by the current window.

For instance, the first window may be a form that has a button that opens a
second window with a select box containing a list of options to choose from.
The first window hasn't yet closed but is waiting for the second window to
provide the user selected choice. At this point, the second window is the
second and top-most window on the stack. Any events that are triggered are now
given to this window. It may completely cover the first window or might only
cover a portion of it being centered on the screen with the edges revealing the
first window behind it. This second window may contain a select box with a list
of several objects or strings to pass back to the first window. One of these
options might be 'new', indicating that the user wishes to create a new string
or object. Selecting this item, might open a third window for this task,
putting this third window on top of the stack. This stacking could go on
indefinitely with each window appending to the ``App.window_stack``. When the
topmost window is closed, this window is 'popped' from the stack and the next
window down in the stack is given back the focus. When an ``App`` no longer has
any windows, the application is closed.

The ``Window`` class is the container class for the widgets. It sets the bounds
for where a widget can be drawn. It may have a border and title set. Note that
this is not the same thing as the curses window object. Although it should have
a reference to this object in ``Window.screen``.

A widget is a user interface object that can be displayed in a window. It is
defined by its height and width, its location on the window, and its foreground
and background colors. It has contents such as a string of text or a more
complicated widget may contain other widgets. In fact, a ``Window`` class is
actually a special kind of top-level widget. You can create your own custom
widgets by extending ``widget.Base``, although nwid comes with a number of
useful generic widgets such as ``TextBox``, ``LabledTextBox``, ``CheckBox``,
``String``, ``Button``, ``Label``, and ``SelectBox``. Widgets can register
events to callback functions in order to handle keyboard or mouse events.


The App Module
--------------

The ``nwid.app`` module comprises


The ``App`` controller is also responsible for the event loop that catches
keyboard and mouse events. It passes these events to the window in focus
(``App.window``) for the window to handle.

Lastly, the ``App`` is responsible for setting up and tearing down the curses
environment. It initializes the curses screen and binds this object to any
window that is put in the window stack. This is done using a ``CursesManager``
object, which is both a context manager and a wrapper for the curses library.
This object is part of the nwid internals and generally doesn't need to be
accessed directly. It takes care of the nitty-gritty details.

The App Class
~~~~~~~~~~~~~

The ``nwid.App`` class is the primary

You can either use it as is or you can inherit from ``App``.

.. code:: python

    >>>

The current window or top-most window is always the window with the focus,
meaning that any events that are triggered are given only to that window. The
``App.window`` attribute always points to this window. Setting this attribute
to a new window will automatically make this new window the window with the
focus and put it on top of the 'window stack'.



Attributes
``````````

Methods
```````

The CursesManager Context Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO

The Event Loop
~~~~~~~~~~~~~~

The event loop is inspired by the design of an Internet browser's event loop.

Registering Events
``````````````````

A widget can register an event with a callback function by

Example:

.. code:: python

    >>> def widget.callback_function(self):
    >>>     print 'Event triggered!'

    >>> widget.register_event('x', widget.callback_function)

Event Propagation
`````````````````

When an event is fired, the main window's trigger function is called with the
event name. It then calls the trigger function of its child that has focus. If
this child has a child widget, the process continues down until it gets to the
lowest widget in focus that has no children. This widget attempts to run any
registered callback functions. The function may return as normal and the parent
regains control and attempts to run any registered callback function that it
may have. This process continues until the main window regains control or if
the exception ``PreventDefault`` is raised. A callback function may choose to
raise ``PreventDefault`` in order to prevent other callback functions from
interferring. This is very similar to JavaScript's ``Event.preventDefault()``
method.



Widget Module
-------------

A Widget is a reusable modular component that is displayed on the screen as a
button, a text field, or other graphical interface. It can be combined to make
a more complex widget component. The widgets that make up this more comlpex
component are the ``children`` widgets to the ``parent`` widget.

The ``parent`` widget is responsible for the layout of its ``children``. The
``parent`` controls the vertical and horizontal alignment as well as whether or
not it has the ability to scroll.

Base Widget
~~~~~~~~~~~

The ``nwid.widget.Base`` class is the foundation for all other widgets. If you
wish to create your own widget, you should inherit from ``Base``.

For example:

.. code:: python

    >>>

String Widget
~~~~~~~~~~~

The ``nwid.widget.String`` class is a basic string widget. This widget is used
for displaying strings.

TextBox Widget
~~~~~~~~~~~~~~

The ``nwid.widget.TextBox`` class is a textbox widget for accepting user input.

ComboBox Widget
~~~~~~~~~~~~~~~

The ``nwid.widget.ComboBox`` class is a textbox widget for accepting user input.

----

Soli Deo gloria.
