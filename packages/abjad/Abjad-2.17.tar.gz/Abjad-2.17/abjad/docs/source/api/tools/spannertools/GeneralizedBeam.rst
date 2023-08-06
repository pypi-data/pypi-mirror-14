.. currentmodule:: abjad.tools.spannertools

GeneralizedBeam
===============

.. autoclass:: GeneralizedBeam

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
              "abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>GeneralizedBeam</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Spanner.Spanner" [color=3,
                  group=2,
                  label=Spanner,
                  shape=box];
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam";
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

      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.components
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.durations
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.include_long_duration_notes
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.include_long_duration_rests
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.isolated_nib_direction
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.name
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.overrides
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.use_stemlets
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.vertical_direction
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__contains__
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__copy__
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__eq__
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__format__
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__getitem__
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__hash__
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__len__
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__lt__
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__ne__
      ~abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.components

.. autoattribute:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.durations

.. autoattribute:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.include_long_duration_notes

.. autoattribute:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.include_long_duration_rests

.. autoattribute:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.isolated_nib_direction

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.overrides

.. autoattribute:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.use_stemlets

.. autoattribute:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.vertical_direction

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam.__repr__
