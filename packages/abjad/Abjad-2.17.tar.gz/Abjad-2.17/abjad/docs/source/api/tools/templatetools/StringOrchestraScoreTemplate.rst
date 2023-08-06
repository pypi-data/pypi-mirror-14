.. currentmodule:: abjad.tools.templatetools

StringOrchestraScoreTemplate
============================

.. autoclass:: StringOrchestraScoreTemplate

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
          subgraph cluster_templatetools {
              graph [label=templatetools];
              "abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>StringOrchestraScoreTemplate</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate";
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

      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.cello_count
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.context_name_abbreviations
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.contrabass_count
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.split_hands
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.use_percussion_clefs
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.viola_count
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.violin_count
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__call__
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__copy__
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__eq__
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__format__
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__hash__
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__ne__
      ~abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.cello_count

.. autoattribute:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.context_name_abbreviations

.. autoattribute:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.contrabass_count

.. autoattribute:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.split_hands

.. autoattribute:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.use_percussion_clefs

.. autoattribute:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.viola_count

.. autoattribute:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.violin_count

Special methods
---------------

.. automethod:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate.__repr__
