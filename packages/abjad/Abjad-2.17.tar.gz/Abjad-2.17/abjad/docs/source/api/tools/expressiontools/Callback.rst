.. currentmodule:: abjad.tools.expressiontools

Callback
========

.. autoclass:: Callback

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
          subgraph cluster_expressiontools {
              graph [label=expressiontools];
              "abjad.tools.expressiontools.Callback.Callback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Callback</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.expressiontools.Callback.Callback";
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

      ~abjad.tools.expressiontools.Callback.Callback.arguments
      ~abjad.tools.expressiontools.Callback.Callback.module_names
      ~abjad.tools.expressiontools.Callback.Callback.name
      ~abjad.tools.expressiontools.Callback.Callback.__call__
      ~abjad.tools.expressiontools.Callback.Callback.__eq__
      ~abjad.tools.expressiontools.Callback.Callback.__format__
      ~abjad.tools.expressiontools.Callback.Callback.__hash__
      ~abjad.tools.expressiontools.Callback.Callback.__ne__
      ~abjad.tools.expressiontools.Callback.Callback.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.expressiontools.Callback.Callback.arguments

.. autoattribute:: abjad.tools.expressiontools.Callback.Callback.module_names

.. autoattribute:: abjad.tools.expressiontools.Callback.Callback.name

Special methods
---------------

.. automethod:: abjad.tools.expressiontools.Callback.Callback.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.Callback.Callback.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.Callback.Callback.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.Callback.Callback.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.Callback.Callback.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.Callback.Callback.__repr__
