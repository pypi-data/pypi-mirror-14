.. currentmodule:: abjad.tools.rhythmmakertools

BeamSpecifier
=============

.. autoclass:: BeamSpecifier

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
              "abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>BeamSpecifier</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.beam_divisions_together
      ~abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.beam_each_division
      ~abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.beam_rests
      ~abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.stemlet_length
      ~abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.use_feather_beams
      ~abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.__copy__
      ~abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.__eq__
      ~abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.__format__
      ~abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.__hash__
      ~abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.__ne__
      ~abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.beam_divisions_together

.. autoattribute:: abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.beam_each_division

.. autoattribute:: abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.beam_rests

.. autoattribute:: abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.stemlet_length

.. autoattribute:: abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.use_feather_beams

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.__copy__

.. automethod:: abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.__eq__

.. automethod:: abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.__format__

.. automethod:: abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.__ne__

.. automethod:: abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier.__repr__
