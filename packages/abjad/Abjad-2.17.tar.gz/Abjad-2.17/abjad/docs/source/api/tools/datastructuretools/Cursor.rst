.. currentmodule:: abjad.tools.datastructuretools

Cursor
======

.. autoclass:: Cursor

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
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.Cursor.Cursor" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Cursor</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.Cursor.Cursor";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.datastructuretools.Cursor.Cursor.next
      ~abjad.tools.datastructuretools.Cursor.Cursor.position
      ~abjad.tools.datastructuretools.Cursor.Cursor.source
      ~abjad.tools.datastructuretools.Cursor.Cursor.__eq__
      ~abjad.tools.datastructuretools.Cursor.Cursor.__format__
      ~abjad.tools.datastructuretools.Cursor.Cursor.__hash__
      ~abjad.tools.datastructuretools.Cursor.Cursor.__ne__
      ~abjad.tools.datastructuretools.Cursor.Cursor.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.datastructuretools.Cursor.Cursor.position

.. autoattribute:: abjad.tools.datastructuretools.Cursor.Cursor.source

Methods
-------

.. automethod:: abjad.tools.datastructuretools.Cursor.Cursor.next

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.Cursor.Cursor.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Cursor.Cursor.__format__

.. automethod:: abjad.tools.datastructuretools.Cursor.Cursor.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Cursor.Cursor.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.Cursor.Cursor.__repr__
