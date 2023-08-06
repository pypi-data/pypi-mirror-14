.. currentmodule:: abjad.tools.pitchtools

PitchArrayCell
==============

.. autoclass:: PitchArrayCell

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
              "abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>PitchArrayCell</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell";
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

      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.append_pitch
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.column_indices
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.column_start_index
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.column_stop_index
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.indices
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.is_first_in_row
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.is_last_in_row
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.item
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.matches_cell
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.next
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.parent_array
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.parent_column
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.parent_row
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.pitches
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.previous
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.row_index
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.weight
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.width
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.__eq__
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.__format__
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.__hash__
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.__ne__
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.__repr__
      ~abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.column_indices

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.column_start_index

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.column_stop_index

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.indices

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.is_first_in_row

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.is_last_in_row

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.item

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.next

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.parent_array

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.parent_column

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.parent_row

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.previous

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.row_index

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.weight

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.width

Read/write properties
---------------------

.. autoattribute:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.pitches

Methods
-------

.. automethod:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.append_pitch

.. automethod:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.matches_cell

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.__repr__

.. automethod:: abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell.__str__
