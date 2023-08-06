.. currentmodule:: abjad.tools.spannertools

ComplexBeam
===========

.. autoclass:: ComplexBeam

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
              "abjad.tools.spannertools.Beam.Beam" [color=3,
                  group=2,
                  label=Beam,
                  shape=box];
              "abjad.tools.spannertools.ComplexBeam.ComplexBeam" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ComplexBeam</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.DuratedComplexBeam.DuratedComplexBeam" [color=3,
                  group=2,
                  label=DuratedComplexBeam,
                  shape=box];
              "abjad.tools.spannertools.MeasuredComplexBeam.MeasuredComplexBeam" [color=3,
                  group=2,
                  label=MeasuredComplexBeam,
                  shape=box];
              "abjad.tools.spannertools.Spanner.Spanner" [color=3,
                  group=2,
                  label=Spanner,
                  shape=box];
              "abjad.tools.spannertools.Beam.Beam" -> "abjad.tools.spannertools.ComplexBeam.ComplexBeam";
              "abjad.tools.spannertools.ComplexBeam.ComplexBeam" -> "abjad.tools.spannertools.DuratedComplexBeam.DuratedComplexBeam";
              "abjad.tools.spannertools.ComplexBeam.ComplexBeam" -> "abjad.tools.spannertools.MeasuredComplexBeam.MeasuredComplexBeam";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Beam.Beam";
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

- :py:class:`abjad.tools.spannertools.Beam`

- :py:class:`abjad.tools.spannertools.Spanner`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.components
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.direction
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.isolated_nib_direction
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.name
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.overrides
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.__contains__
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.__copy__
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.__eq__
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.__format__
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.__getitem__
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.__hash__
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.__len__
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.__lt__
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.__ne__
      ~abjad.tools.spannertools.ComplexBeam.ComplexBeam.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.components

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.direction

.. autoattribute:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.isolated_nib_direction

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.overrides

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.ComplexBeam.ComplexBeam.__repr__
