.. currentmodule:: abjad.tools.pitchtools

PitchArrayColumn
================

.. autoclass:: PitchArrayColumn

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
              "abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>PitchArrayColumn</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn";
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

      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.append
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.cell_tokens
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.cell_widths
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.cells
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.column_index
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.depth
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.dimensions
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.extend
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.has_voice_crossing
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.is_defective
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.parent_array
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.pitches
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.remove_pitches
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.start_cells
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.start_pitches
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.stop_cells
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.stop_pitches
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.weight
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.width
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__eq__
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__format__
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__getitem__
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__hash__
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__ne__
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__repr__
      ~abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.cell_tokens

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.cell_widths

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.cells

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.column_index

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.depth

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.dimensions

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.has_voice_crossing

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.is_defective

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.parent_array

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.pitches

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.start_cells

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.start_pitches

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.stop_cells

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.stop_pitches

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.weight

.. autoattribute:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.width

Methods
-------

.. automethod:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.append

.. automethod:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.extend

.. automethod:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.remove_pitches

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__format__

.. automethod:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__getitem__

.. automethod:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__hash__

.. automethod:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__repr__

.. automethod:: abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn.__str__
