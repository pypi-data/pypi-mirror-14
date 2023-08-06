.. currentmodule:: abjad.tools.systemtools

WellformednessManager
=====================

.. autoclass:: WellformednessManager

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
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.WellformednessManager.WellformednessManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>WellformednessManager</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.WellformednessManager.WellformednessManager";
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

      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_beamed_quarter_notes
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_conflicting_clefs
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_discontiguous_spanners
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_duplicate_ids
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_empty_containers
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_intermarked_hairpins
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_misdurated_measures
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_misfilled_measures
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_mismatched_enchained_hairpins
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_mispitched_ties
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_misrepresented_flags
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_missing_parents
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_nested_measures
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_overlapping_beams
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_overlapping_glissandi
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_overlapping_hairpins
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_overlapping_octavation_spanners
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_overlapping_ties
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_short_hairpins
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_tied_rests
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.__call__
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.__eq__
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.__format__
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.__hash__
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.__ne__
      ~abjad.tools.systemtools.WellformednessManager.WellformednessManager.__repr__

Methods
-------

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_beamed_quarter_notes

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_conflicting_clefs

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_discontiguous_spanners

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_duplicate_ids

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_empty_containers

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_intermarked_hairpins

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_misdurated_measures

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_misfilled_measures

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_mismatched_enchained_hairpins

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_mispitched_ties

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_misrepresented_flags

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_missing_parents

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_nested_measures

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_overlapping_beams

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_overlapping_glissandi

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_overlapping_hairpins

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_overlapping_octavation_spanners

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_overlapping_ties

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_short_hairpins

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.check_tied_rests

Special methods
---------------

.. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.WellformednessManager.WellformednessManager.__repr__
