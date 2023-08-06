.. currentmodule:: abjad.tools.pitchtools

NumberedIntervalClass
=====================

.. autoclass:: NumberedIntervalClass

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
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" [color=3,
                  group=2,
                  label=IntervalClass,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NumberedIntervalClass</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NumberedInversionEquivalentIntervalClass.NumberedInversionEquivalentIntervalClass" [color=3,
                  group=2,
                  label=NumberedInversionEquivalentIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" -> "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass";
              "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass" -> "abjad.tools.pitchtools.NumberedInversionEquivalentIntervalClass.NumberedInversionEquivalentIntervalClass";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.IntervalClass.IntervalClass";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.pitchtools.IntervalClass`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.direction_number
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.direction_symbol
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.direction_word
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.from_pitch_carriers
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.number
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__abs__
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__eq__
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__float__
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__format__
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__hash__
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__int__
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__ne__
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__repr__
      ~abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.direction_number

.. autoattribute:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.direction_symbol

.. autoattribute:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.direction_word

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.number

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.from_pitch_carriers

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__abs__

.. automethod:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__eq__

.. automethod:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__format__

.. automethod:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__hash__

.. automethod:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__int__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass.__str__
