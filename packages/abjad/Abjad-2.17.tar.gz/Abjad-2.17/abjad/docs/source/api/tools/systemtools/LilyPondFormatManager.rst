.. currentmodule:: abjad.tools.systemtools

LilyPondFormatManager
=====================

.. autoclass:: LilyPondFormatManager

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
              "abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondFormatManager</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager";
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

      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.bundle_format_contributions
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.format_lilypond_attribute
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.format_lilypond_context_setting_in_with_block
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.format_lilypond_context_setting_inline
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.format_lilypond_value
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.make_lilypond_override_string
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.make_lilypond_revert_string
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.report_component_format_contributions
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.report_spanner_format_contributions
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.__eq__
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.__format__
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.__hash__
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.__ne__
      ~abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.__repr__

Class & static methods
----------------------

.. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.bundle_format_contributions

.. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.format_lilypond_attribute

.. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.format_lilypond_context_setting_in_with_block

.. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.format_lilypond_context_setting_inline

.. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.format_lilypond_value

.. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.make_lilypond_override_string

.. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.make_lilypond_revert_string

.. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.report_component_format_contributions

.. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.report_spanner_format_contributions

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager.__repr__
