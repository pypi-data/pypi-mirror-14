.. currentmodule:: abjad.tools.abjadbooktools

CodeBlockSpecifier
==================

.. autoclass:: CodeBlockSpecifier

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [background=transparent,
              bgcolor=transparent,
              color=lightslategrey,
              fontname=Arial,
              outputorder=edgesfirst,
              overlap=prism,
              penwidth=2,
              rankdir=LR,
              root="__builtin__.object",
              splines=spline,
              style="dotted, rounded",
              truecolor=true];
          node [colorscheme=pastel19,
              fontname=Arial,
              fontsize=12,
              penwidth=2,
              style="filled, rounded"];
          edge [color=lightsteelblue2,
              penwidth=2];
          subgraph cluster_abctools {
              graph [label=abctools];
              "abjad.tools.abctools.AbjadObject.AbjadObject" [color=1,
                  group=0,
                  label=AbjadObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbstractBase" [color=1,
                  group=0,
                  label=AbstractBase,
                  shape=box];
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_abjadbooktools {
              graph [label=abjadbooktools];
              "abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>CodeBlockSpecifier</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=3,
                  group=2,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.allow_exceptions
      ~abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.from_options
      ~abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.hide
      ~abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.strip_prompt
      ~abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.text_width
      ~abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.__copy__
      ~abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.__eq__
      ~abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.__format__
      ~abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.__hash__
      ~abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.__ne__
      ~abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.allow_exceptions

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.hide

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.strip_prompt

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.text_width

Class & static methods
----------------------

.. automethod:: abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.from_options

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier.__repr__
