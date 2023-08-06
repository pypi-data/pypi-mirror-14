.. currentmodule:: abjad.tools.tonalanalysistools

ChordQuality
============

.. autoclass:: ChordQuality

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
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.ChordQuality.ChordQuality" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ChordQuality</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordQuality.ChordQuality";
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

      ~abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.is_uppercase
      ~abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.quality_string
      ~abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.__eq__
      ~abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.__format__
      ~abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.__hash__
      ~abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.__ne__
      ~abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.is_uppercase

.. autoattribute:: abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.quality_string

Special methods
---------------

.. automethod:: abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.__format__

.. automethod:: abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.__hash__

.. automethod:: abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.__ne__

.. automethod:: abjad.tools.tonalanalysistools.ChordQuality.ChordQuality.__repr__
