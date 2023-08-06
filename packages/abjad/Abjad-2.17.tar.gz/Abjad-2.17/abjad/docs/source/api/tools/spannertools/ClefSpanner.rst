.. currentmodule:: abjad.tools.spannertools

ClefSpanner
===========

.. autoclass:: ClefSpanner

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
              "abjad.tools.spannertools.ClefSpanner.ClefSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ClefSpanner</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Spanner.Spanner" [color=3,
                  group=2,
                  label=Spanner,
                  shape=box];
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.ClefSpanner.ClefSpanner";
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

      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.clef
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.components
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.name
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.overrides
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.__contains__
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.__copy__
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.__eq__
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.__format__
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.__getitem__
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.__hash__
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.__len__
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.__lt__
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.__ne__
      ~abjad.tools.spannertools.ClefSpanner.ClefSpanner.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.clef

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.components

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.overrides

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ClefSpanner.ClefSpanner.__repr__
