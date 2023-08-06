.. currentmodule:: abjad.tools.indicatortools

SpacingIndication
=================

.. autoclass:: SpacingIndication

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
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.SpacingIndication.SpacingIndication" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>SpacingIndication</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.indicatortools.SpacingIndication.SpacingIndication";
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

      ~abjad.tools.indicatortools.SpacingIndication.SpacingIndication.normalized_spacing_duration
      ~abjad.tools.indicatortools.SpacingIndication.SpacingIndication.proportional_notation_duration
      ~abjad.tools.indicatortools.SpacingIndication.SpacingIndication.tempo_indication
      ~abjad.tools.indicatortools.SpacingIndication.SpacingIndication.__eq__
      ~abjad.tools.indicatortools.SpacingIndication.SpacingIndication.__format__
      ~abjad.tools.indicatortools.SpacingIndication.SpacingIndication.__hash__
      ~abjad.tools.indicatortools.SpacingIndication.SpacingIndication.__ne__
      ~abjad.tools.indicatortools.SpacingIndication.SpacingIndication.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.indicatortools.SpacingIndication.SpacingIndication.normalized_spacing_duration

.. autoattribute:: abjad.tools.indicatortools.SpacingIndication.SpacingIndication.proportional_notation_duration

.. autoattribute:: abjad.tools.indicatortools.SpacingIndication.SpacingIndication.tempo_indication

Special methods
---------------

.. automethod:: abjad.tools.indicatortools.SpacingIndication.SpacingIndication.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.SpacingIndication.SpacingIndication.__format__

.. automethod:: abjad.tools.indicatortools.SpacingIndication.SpacingIndication.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.SpacingIndication.SpacingIndication.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.SpacingIndication.SpacingIndication.__repr__
