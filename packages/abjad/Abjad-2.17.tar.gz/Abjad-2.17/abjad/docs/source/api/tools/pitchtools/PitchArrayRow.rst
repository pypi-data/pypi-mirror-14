.. currentmodule:: abjad.tools.pitchtools

PitchArrayRow
=============

.. autoclass:: PitchArrayRow

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
              "abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>PitchArrayRow</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow";
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

      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.append
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.apply_pitches
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.cell_tokens
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.cell_widths
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.cells
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.copy_subrow
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.depth
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.dimensions
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.empty_pitches
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.extend
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.has_spanning_cell_over_index
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.index
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.is_defective
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.is_in_range
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.merge
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.pad_to_width
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.parent_array
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.pitch_range
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.pitches
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.pop
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.remove
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.row_index
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.to_measure
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.weight
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.width
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.withdraw
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__add__
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__copy__
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__eq__
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__format__
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__getitem__
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__hash__
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__iadd__
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__iter__
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__len__
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__ne__
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__repr__
      ~abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.cell_tokens

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.cell_widths

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.cells

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.depth

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.dimensions

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.is_defective

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.is_in_range

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.parent_array

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.pitches

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.row_index

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.weight

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.width

Read/write properties
---------------------

.. autoattribute:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.pitch_range

Methods
-------

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.append

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.apply_pitches

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.copy_subrow

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.empty_pitches

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.extend

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.has_spanning_cell_over_index

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.index

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.merge

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.pad_to_width

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.pop

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.remove

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.to_measure

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.withdraw

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__add__

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__copy__

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__format__

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__getitem__

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__hash__

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__iadd__

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__iter__

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__len__

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__repr__

.. automethod:: abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow.__str__
