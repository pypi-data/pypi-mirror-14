.. currentmodule:: abjad.tools.rhythmmakertools

SkipRhythmMaker
===============

.. autoclass:: SkipRhythmMaker

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
              "abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>SkipRhythmMaker</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker";
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

      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.beam_specifier
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.division_masks
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.duration_spelling_specifier
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.logical_tie_masks
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.tie_specifier
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.tuplet_spelling_specifier
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__call__
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__copy__
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__eq__
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__format__
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__hash__
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__illustrate__
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__ne__
      ~abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.beam_specifier

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.division_masks

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.duration_spelling_specifier

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.logical_tie_masks

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.tie_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.tuplet_spelling_specifier

Special methods
---------------

.. automethod:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__eq__

.. automethod:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker.__repr__
