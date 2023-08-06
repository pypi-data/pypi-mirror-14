.. currentmodule:: abjad.tools.pitchtools

Interval
========

.. autoclass:: Interval

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
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.Interval.Interval" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Interval</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NamedInterval.NamedInterval" [color=3,
                  group=2,
                  label=NamedInterval,
                  shape=box];
              "abjad.tools.pitchtools.NumberedInterval.NumberedInterval" [color=3,
                  group=2,
                  label=NumberedInterval,
                  shape=box];
              "abjad.tools.pitchtools.Interval.Interval" -> "abjad.tools.pitchtools.NamedInterval.NamedInterval";
              "abjad.tools.pitchtools.Interval.Interval" -> "abjad.tools.pitchtools.NumberedInterval.NumberedInterval";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.Interval.Interval";
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

      ~abjad.tools.pitchtools.Interval.Interval.cents
      ~abjad.tools.pitchtools.Interval.Interval.is_named_interval_abbreviation
      ~abjad.tools.pitchtools.Interval.Interval.is_named_interval_quality_abbreviation
      ~abjad.tools.pitchtools.Interval.Interval.__abs__
      ~abjad.tools.pitchtools.Interval.Interval.__eq__
      ~abjad.tools.pitchtools.Interval.Interval.__float__
      ~abjad.tools.pitchtools.Interval.Interval.__format__
      ~abjad.tools.pitchtools.Interval.Interval.__hash__
      ~abjad.tools.pitchtools.Interval.Interval.__int__
      ~abjad.tools.pitchtools.Interval.Interval.__ne__
      ~abjad.tools.pitchtools.Interval.Interval.__neg__
      ~abjad.tools.pitchtools.Interval.Interval.__repr__
      ~abjad.tools.pitchtools.Interval.Interval.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.Interval.Interval.cents

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.Interval.Interval.is_named_interval_abbreviation

.. automethod:: abjad.tools.pitchtools.Interval.Interval.is_named_interval_quality_abbreviation

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.Interval.Interval.__abs__

.. automethod:: abjad.tools.pitchtools.Interval.Interval.__eq__

.. automethod:: abjad.tools.pitchtools.Interval.Interval.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Interval.Interval.__format__

.. automethod:: abjad.tools.pitchtools.Interval.Interval.__hash__

.. automethod:: abjad.tools.pitchtools.Interval.Interval.__int__

.. automethod:: abjad.tools.pitchtools.Interval.Interval.__ne__

.. automethod:: abjad.tools.pitchtools.Interval.Interval.__neg__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Interval.Interval.__repr__

.. automethod:: abjad.tools.pitchtools.Interval.Interval.__str__
