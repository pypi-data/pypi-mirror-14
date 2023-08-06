.. currentmodule:: abjad.tools.rhythmmakertools

TaleaRhythmMaker
================

.. autoclass:: TaleaRhythmMaker

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" [color=3,
                  group=2,
                  label=RhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TaleaRhythmMaker</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.rhythmmakertools.RhythmMaker`

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.beam_specifier
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.burnish_specifier
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.division_masks
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.duration_spelling_specifier
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.extra_counts_per_division
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.helper_functions
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.logical_tie_masks
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.read_talea_once_only
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.rest_tied_notes
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.split_divisions_by_counts
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.talea
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.tie_specifier
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.tie_split_notes
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.tuplet_spelling_specifier
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__call__
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__copy__
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__eq__
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__format__
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__hash__
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__illustrate__
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__ne__
      ~abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.beam_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.burnish_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.division_masks

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.duration_spelling_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.extra_counts_per_division

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.helper_functions

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.logical_tie_masks

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.read_talea_once_only

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.rest_tied_notes

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.split_divisions_by_counts

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.talea

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.tie_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.tie_split_notes

.. autoattribute:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.tuplet_spelling_specifier

Special methods
---------------

.. automethod:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__eq__

.. automethod:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__hash__

.. automethod:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__ne__

.. automethod:: abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker.__repr__
