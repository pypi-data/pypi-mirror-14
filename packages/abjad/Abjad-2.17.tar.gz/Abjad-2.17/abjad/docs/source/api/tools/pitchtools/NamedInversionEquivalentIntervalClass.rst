.. currentmodule:: abjad.tools.pitchtools

NamedInversionEquivalentIntervalClass
=====================================

.. autoclass:: NamedInversionEquivalentIntervalClass

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
              "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass" [color=3,
                  group=2,
                  label=NamedIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NamedInversionEquivalentIntervalClass</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" -> "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass";
              "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass" -> "abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass";
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

- :py:class:`abjad.tools.pitchtools.NamedIntervalClass`

- :py:class:`abjad.tools.pitchtools.IntervalClass`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.direction_number
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.direction_string
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.direction_symbol
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.from_pitch_carriers
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.number
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.quality_string
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__abs__
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__eq__
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__float__
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__format__
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__hash__
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__int__
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__lt__
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__ne__
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__repr__
      ~abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__str__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.direction_number

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.direction_string

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.direction_symbol

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.number

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.quality_string

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.from_pitch_carriers

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__abs__

.. automethod:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__format__

.. automethod:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__int__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__lt__

.. automethod:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass.__str__
