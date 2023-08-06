.. currentmodule:: abjad.tools.spannertools

Crescendo
=========

.. autoclass:: Crescendo

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
              "abjad.tools.spannertools.Crescendo.Crescendo" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Crescendo</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Hairpin.Hairpin" [color=3,
                  group=2,
                  label=Hairpin,
                  shape=box];
              "abjad.tools.spannertools.Spanner.Spanner" [color=3,
                  group=2,
                  label=Spanner,
                  shape=box];
              "abjad.tools.spannertools.Hairpin.Hairpin" -> "abjad.tools.spannertools.Crescendo.Crescendo";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Hairpin.Hairpin";
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

- :py:class:`abjad.tools.spannertools.Hairpin`

- :py:class:`abjad.tools.spannertools.Spanner`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.spannertools.Crescendo.Crescendo.components
      ~abjad.tools.spannertools.Crescendo.Crescendo.descriptor
      ~abjad.tools.spannertools.Crescendo.Crescendo.direction
      ~abjad.tools.spannertools.Crescendo.Crescendo.include_rests
      ~abjad.tools.spannertools.Crescendo.Crescendo.name
      ~abjad.tools.spannertools.Crescendo.Crescendo.overrides
      ~abjad.tools.spannertools.Crescendo.Crescendo.shape_string
      ~abjad.tools.spannertools.Crescendo.Crescendo.start_dynamic
      ~abjad.tools.spannertools.Crescendo.Crescendo.stop_dynamic
      ~abjad.tools.spannertools.Crescendo.Crescendo.__contains__
      ~abjad.tools.spannertools.Crescendo.Crescendo.__copy__
      ~abjad.tools.spannertools.Crescendo.Crescendo.__eq__
      ~abjad.tools.spannertools.Crescendo.Crescendo.__format__
      ~abjad.tools.spannertools.Crescendo.Crescendo.__getitem__
      ~abjad.tools.spannertools.Crescendo.Crescendo.__hash__
      ~abjad.tools.spannertools.Crescendo.Crescendo.__len__
      ~abjad.tools.spannertools.Crescendo.Crescendo.__lt__
      ~abjad.tools.spannertools.Crescendo.Crescendo.__ne__
      ~abjad.tools.spannertools.Crescendo.Crescendo.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.Crescendo.Crescendo.components

.. autoattribute:: abjad.tools.spannertools.Crescendo.Crescendo.descriptor

.. autoattribute:: abjad.tools.spannertools.Crescendo.Crescendo.direction

.. autoattribute:: abjad.tools.spannertools.Crescendo.Crescendo.include_rests

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.Crescendo.Crescendo.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.Crescendo.Crescendo.overrides

.. autoattribute:: abjad.tools.spannertools.Crescendo.Crescendo.shape_string

.. autoattribute:: abjad.tools.spannertools.Crescendo.Crescendo.start_dynamic

.. autoattribute:: abjad.tools.spannertools.Crescendo.Crescendo.stop_dynamic

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Crescendo.Crescendo.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Crescendo.Crescendo.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Crescendo.Crescendo.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Crescendo.Crescendo.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Crescendo.Crescendo.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Crescendo.Crescendo.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Crescendo.Crescendo.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Crescendo.Crescendo.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Crescendo.Crescendo.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Crescendo.Crescendo.__repr__
