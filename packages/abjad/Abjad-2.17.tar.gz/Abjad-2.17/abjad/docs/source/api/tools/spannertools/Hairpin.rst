.. currentmodule:: abjad.tools.spannertools

Hairpin
=======

.. autoclass:: Hairpin

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
              "abjad.tools.spannertools.Crescendo.Crescendo" [color=3,
                  group=2,
                  label=Crescendo,
                  shape=box];
              "abjad.tools.spannertools.Decrescendo.Decrescendo" [color=3,
                  group=2,
                  label=Decrescendo,
                  shape=box];
              "abjad.tools.spannertools.Hairpin.Hairpin" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Hairpin</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Spanner.Spanner" [color=3,
                  group=2,
                  label=Spanner,
                  shape=box];
              "abjad.tools.spannertools.Hairpin.Hairpin" -> "abjad.tools.spannertools.Crescendo.Crescendo";
              "abjad.tools.spannertools.Hairpin.Hairpin" -> "abjad.tools.spannertools.Decrescendo.Decrescendo";
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

- :py:class:`abjad.tools.spannertools.Spanner`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.spannertools.Hairpin.Hairpin.components
      ~abjad.tools.spannertools.Hairpin.Hairpin.descriptor
      ~abjad.tools.spannertools.Hairpin.Hairpin.direction
      ~abjad.tools.spannertools.Hairpin.Hairpin.include_rests
      ~abjad.tools.spannertools.Hairpin.Hairpin.name
      ~abjad.tools.spannertools.Hairpin.Hairpin.overrides
      ~abjad.tools.spannertools.Hairpin.Hairpin.shape_string
      ~abjad.tools.spannertools.Hairpin.Hairpin.start_dynamic
      ~abjad.tools.spannertools.Hairpin.Hairpin.stop_dynamic
      ~abjad.tools.spannertools.Hairpin.Hairpin.__contains__
      ~abjad.tools.spannertools.Hairpin.Hairpin.__copy__
      ~abjad.tools.spannertools.Hairpin.Hairpin.__eq__
      ~abjad.tools.spannertools.Hairpin.Hairpin.__format__
      ~abjad.tools.spannertools.Hairpin.Hairpin.__getitem__
      ~abjad.tools.spannertools.Hairpin.Hairpin.__hash__
      ~abjad.tools.spannertools.Hairpin.Hairpin.__len__
      ~abjad.tools.spannertools.Hairpin.Hairpin.__lt__
      ~abjad.tools.spannertools.Hairpin.Hairpin.__ne__
      ~abjad.tools.spannertools.Hairpin.Hairpin.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.Hairpin.Hairpin.components

.. autoattribute:: abjad.tools.spannertools.Hairpin.Hairpin.descriptor

.. autoattribute:: abjad.tools.spannertools.Hairpin.Hairpin.direction

.. autoattribute:: abjad.tools.spannertools.Hairpin.Hairpin.include_rests

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.Hairpin.Hairpin.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.Hairpin.Hairpin.overrides

.. autoattribute:: abjad.tools.spannertools.Hairpin.Hairpin.shape_string

.. autoattribute:: abjad.tools.spannertools.Hairpin.Hairpin.start_dynamic

.. autoattribute:: abjad.tools.spannertools.Hairpin.Hairpin.stop_dynamic

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Hairpin.Hairpin.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Hairpin.Hairpin.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Hairpin.Hairpin.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Hairpin.Hairpin.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Hairpin.Hairpin.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Hairpin.Hairpin.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Hairpin.Hairpin.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Hairpin.Hairpin.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Hairpin.Hairpin.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Hairpin.Hairpin.__repr__
