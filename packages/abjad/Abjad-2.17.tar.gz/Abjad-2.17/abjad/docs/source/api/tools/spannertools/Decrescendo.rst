.. currentmodule:: abjad.tools.spannertools

Decrescendo
===========

.. autoclass:: Decrescendo

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
              "abjad.tools.spannertools.Decrescendo.Decrescendo" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Decrescendo</B>>,
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

- :py:class:`abjad.tools.spannertools.Hairpin`

- :py:class:`abjad.tools.spannertools.Spanner`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.spannertools.Decrescendo.Decrescendo.components
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.descriptor
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.direction
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.include_rests
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.name
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.overrides
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.shape_string
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.start_dynamic
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.stop_dynamic
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.__contains__
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.__copy__
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.__eq__
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.__format__
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.__getitem__
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.__hash__
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.__len__
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.__lt__
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.__ne__
      ~abjad.tools.spannertools.Decrescendo.Decrescendo.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.Decrescendo.Decrescendo.components

.. autoattribute:: abjad.tools.spannertools.Decrescendo.Decrescendo.descriptor

.. autoattribute:: abjad.tools.spannertools.Decrescendo.Decrescendo.direction

.. autoattribute:: abjad.tools.spannertools.Decrescendo.Decrescendo.include_rests

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.Decrescendo.Decrescendo.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.Decrescendo.Decrescendo.overrides

.. autoattribute:: abjad.tools.spannertools.Decrescendo.Decrescendo.shape_string

.. autoattribute:: abjad.tools.spannertools.Decrescendo.Decrescendo.start_dynamic

.. autoattribute:: abjad.tools.spannertools.Decrescendo.Decrescendo.stop_dynamic

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Decrescendo.Decrescendo.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Decrescendo.Decrescendo.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Decrescendo.Decrescendo.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Decrescendo.Decrescendo.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Decrescendo.Decrescendo.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Decrescendo.Decrescendo.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Decrescendo.Decrescendo.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Decrescendo.Decrescendo.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Decrescendo.Decrescendo.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Decrescendo.Decrescendo.__repr__
