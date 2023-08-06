.. currentmodule:: abjad.tools.rhythmmakertools

IncisedRhythmMaker
==================

.. autoclass:: IncisedRhythmMaker

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
              "abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>IncisedRhythmMaker</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" [color=3,
                  group=2,
                  label=RhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker";
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

      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.beam_specifier
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.division_masks
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.duration_spelling_specifier
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.extra_counts_per_division
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.helper_functions
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.incise_specifier
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.logical_tie_masks
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.replace_rests_with_skips
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.split_divisions_by_counts
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.tie_specifier
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.tuplet_spelling_specifier
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__call__
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__copy__
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__eq__
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__format__
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__hash__
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__illustrate__
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__ne__
      ~abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.beam_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.division_masks

.. autoattribute:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.duration_spelling_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.extra_counts_per_division

.. autoattribute:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.helper_functions

.. autoattribute:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.incise_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.logical_tie_masks

.. autoattribute:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.replace_rests_with_skips

.. autoattribute:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.split_divisions_by_counts

.. autoattribute:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.tie_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.tuplet_spelling_specifier

Special methods
---------------

.. automethod:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker.__repr__
