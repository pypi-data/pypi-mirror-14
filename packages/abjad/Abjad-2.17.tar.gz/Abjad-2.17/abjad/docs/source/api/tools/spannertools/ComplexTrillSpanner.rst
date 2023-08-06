.. currentmodule:: abjad.tools.spannertools

ComplexTrillSpanner
===================

.. autoclass:: ComplexTrillSpanner

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
          subgraph cluster_spannertools {
              graph [label=spannertools];
              "abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ComplexTrillSpanner</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Spanner.Spanner" [color=3,
                  group=2,
                  label=Spanner,
                  shape=box];
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.spannertools.Spanner.Spanner";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.spannertools.Spanner`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.components
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.interval
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.name
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.overrides
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__contains__
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__copy__
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__eq__
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__format__
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__getitem__
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__hash__
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__len__
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__lt__
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__ne__
      ~abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.components

.. autoattribute:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.interval

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.overrides

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner.__repr__
