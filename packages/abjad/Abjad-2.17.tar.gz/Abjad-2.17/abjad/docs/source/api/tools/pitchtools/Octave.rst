.. currentmodule:: abjad.tools.pitchtools

Octave
======

.. autoclass:: Octave

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
              "abjad.tools.pitchtools.Octave.Octave" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Octave</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.Octave.Octave";
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

      ~abjad.tools.pitchtools.Octave.Octave.from_pitch_name
      ~abjad.tools.pitchtools.Octave.Octave.from_pitch_number
      ~abjad.tools.pitchtools.Octave.Octave.is_octave_tick_string
      ~abjad.tools.pitchtools.Octave.Octave.octave_number
      ~abjad.tools.pitchtools.Octave.Octave.octave_tick_string
      ~abjad.tools.pitchtools.Octave.Octave.pitch_number
      ~abjad.tools.pitchtools.Octave.Octave.pitch_range
      ~abjad.tools.pitchtools.Octave.Octave.__eq__
      ~abjad.tools.pitchtools.Octave.Octave.__float__
      ~abjad.tools.pitchtools.Octave.Octave.__format__
      ~abjad.tools.pitchtools.Octave.Octave.__hash__
      ~abjad.tools.pitchtools.Octave.Octave.__int__
      ~abjad.tools.pitchtools.Octave.Octave.__ne__
      ~abjad.tools.pitchtools.Octave.Octave.__repr__
      ~abjad.tools.pitchtools.Octave.Octave.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.Octave.Octave.octave_number

.. autoattribute:: abjad.tools.pitchtools.Octave.Octave.octave_tick_string

.. autoattribute:: abjad.tools.pitchtools.Octave.Octave.pitch_number

.. autoattribute:: abjad.tools.pitchtools.Octave.Octave.pitch_range

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.Octave.Octave.from_pitch_name

.. automethod:: abjad.tools.pitchtools.Octave.Octave.from_pitch_number

.. automethod:: abjad.tools.pitchtools.Octave.Octave.is_octave_tick_string

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.Octave.Octave.__eq__

.. automethod:: abjad.tools.pitchtools.Octave.Octave.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Octave.Octave.__format__

.. automethod:: abjad.tools.pitchtools.Octave.Octave.__hash__

.. automethod:: abjad.tools.pitchtools.Octave.Octave.__int__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Octave.Octave.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Octave.Octave.__repr__

.. automethod:: abjad.tools.pitchtools.Octave.Octave.__str__
