.. currentmodule:: abjad.tools.rhythmmakertools

AccelerandoRhythmMaker
======================

.. autoclass:: AccelerandoRhythmMaker

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
              "abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>AccelerandoRhythmMaker</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" [color=3,
                  group=2,
                  label=RhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker";
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

      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.beam_specifier
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.division_masks
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.duration_spelling_specifier
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.interpolation_specifiers
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.logical_tie_masks
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.tie_specifier
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.tuplet_spelling_specifier
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__call__
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__copy__
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__eq__
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__format__
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__hash__
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__illustrate__
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__ne__
      ~abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.beam_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.division_masks

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.duration_spelling_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.interpolation_specifiers

.. autoattribute:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.logical_tie_masks

.. autoattribute:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.tie_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.tuplet_spelling_specifier

Special methods
---------------

.. automethod:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker.__repr__
