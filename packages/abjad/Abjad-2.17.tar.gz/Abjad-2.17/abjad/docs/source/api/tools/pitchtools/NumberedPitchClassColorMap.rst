.. currentmodule:: abjad.tools.pitchtools

NumberedPitchClassColorMap
==========================

.. autoclass:: NumberedPitchClassColorMap

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
              "abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NumberedPitchClassColorMap</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap";
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

      ~abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.colors
      ~abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.get
      ~abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.is_twelve_tone_complete
      ~abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.is_twenty_four_tone_complete
      ~abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.pairs
      ~abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.pitch_iterables
      ~abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.__eq__
      ~abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.__format__
      ~abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.__getitem__
      ~abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.__hash__
      ~abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.__ne__
      ~abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.colors

.. autoattribute:: abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.is_twelve_tone_complete

.. autoattribute:: abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.is_twenty_four_tone_complete

.. autoattribute:: abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.pairs

.. autoattribute:: abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.pitch_iterables

Methods
-------

.. automethod:: abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.get

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.__format__

.. automethod:: abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap.__repr__
