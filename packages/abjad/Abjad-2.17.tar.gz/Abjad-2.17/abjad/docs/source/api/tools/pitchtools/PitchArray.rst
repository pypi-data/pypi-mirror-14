.. currentmodule:: abjad.tools.pitchtools

PitchArray
==========

.. autoclass:: PitchArray

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
              "abjad.tools.pitchtools.PitchArray.PitchArray" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>PitchArray</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.PitchArray.PitchArray";
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

      ~abjad.tools.pitchtools.PitchArray.PitchArray.append_column
      ~abjad.tools.pitchtools.PitchArray.PitchArray.append_row
      ~abjad.tools.pitchtools.PitchArray.PitchArray.apply_pitches_by_row
      ~abjad.tools.pitchtools.PitchArray.PitchArray.cell_tokens_by_row
      ~abjad.tools.pitchtools.PitchArray.PitchArray.cell_widths_by_row
      ~abjad.tools.pitchtools.PitchArray.PitchArray.cells
      ~abjad.tools.pitchtools.PitchArray.PitchArray.columns
      ~abjad.tools.pitchtools.PitchArray.PitchArray.copy_subarray
      ~abjad.tools.pitchtools.PitchArray.PitchArray.depth
      ~abjad.tools.pitchtools.PitchArray.PitchArray.dimensions
      ~abjad.tools.pitchtools.PitchArray.PitchArray.from_counts
      ~abjad.tools.pitchtools.PitchArray.PitchArray.from_score
      ~abjad.tools.pitchtools.PitchArray.PitchArray.has_spanning_cell_over_index
      ~abjad.tools.pitchtools.PitchArray.PitchArray.has_voice_crossing
      ~abjad.tools.pitchtools.PitchArray.PitchArray.is_rectangular
      ~abjad.tools.pitchtools.PitchArray.PitchArray.list_nonspanning_subarrays
      ~abjad.tools.pitchtools.PitchArray.PitchArray.pad_to_depth
      ~abjad.tools.pitchtools.PitchArray.PitchArray.pad_to_width
      ~abjad.tools.pitchtools.PitchArray.PitchArray.pitches
      ~abjad.tools.pitchtools.PitchArray.PitchArray.pitches_by_row
      ~abjad.tools.pitchtools.PitchArray.PitchArray.pop_column
      ~abjad.tools.pitchtools.PitchArray.PitchArray.pop_row
      ~abjad.tools.pitchtools.PitchArray.PitchArray.remove_row
      ~abjad.tools.pitchtools.PitchArray.PitchArray.rows
      ~abjad.tools.pitchtools.PitchArray.PitchArray.size
      ~abjad.tools.pitchtools.PitchArray.PitchArray.to_measures
      ~abjad.tools.pitchtools.PitchArray.PitchArray.voice_crossing_count
      ~abjad.tools.pitchtools.PitchArray.PitchArray.weight
      ~abjad.tools.pitchtools.PitchArray.PitchArray.width
      ~abjad.tools.pitchtools.PitchArray.PitchArray.__add__
      ~abjad.tools.pitchtools.PitchArray.PitchArray.__contains__
      ~abjad.tools.pitchtools.PitchArray.PitchArray.__copy__
      ~abjad.tools.pitchtools.PitchArray.PitchArray.__eq__
      ~abjad.tools.pitchtools.PitchArray.PitchArray.__format__
      ~abjad.tools.pitchtools.PitchArray.PitchArray.__getitem__
      ~abjad.tools.pitchtools.PitchArray.PitchArray.__hash__
      ~abjad.tools.pitchtools.PitchArray.PitchArray.__iadd__
      ~abjad.tools.pitchtools.PitchArray.PitchArray.__ne__
      ~abjad.tools.pitchtools.PitchArray.PitchArray.__repr__
      ~abjad.tools.pitchtools.PitchArray.PitchArray.__setitem__
      ~abjad.tools.pitchtools.PitchArray.PitchArray.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.cell_tokens_by_row

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.cell_widths_by_row

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.cells

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.columns

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.depth

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.dimensions

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.has_voice_crossing

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.is_rectangular

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.pitches

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.pitches_by_row

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.rows

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.size

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.voice_crossing_count

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.weight

.. autoattribute:: abjad.tools.pitchtools.PitchArray.PitchArray.width

Methods
-------

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.append_column

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.append_row

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.apply_pitches_by_row

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.copy_subarray

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.has_spanning_cell_over_index

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.list_nonspanning_subarrays

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.pad_to_depth

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.pad_to_width

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.pop_column

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.pop_row

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.remove_row

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.to_measures

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.from_counts

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.from_score

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.__add__

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.__contains__

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.__copy__

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.__format__

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.__getitem__

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.__hash__

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.__iadd__

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.__repr__

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.__setitem__

.. automethod:: abjad.tools.pitchtools.PitchArray.PitchArray.__str__
