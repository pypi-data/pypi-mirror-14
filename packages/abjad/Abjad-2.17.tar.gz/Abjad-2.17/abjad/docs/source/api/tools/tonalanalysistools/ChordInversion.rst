.. currentmodule:: abjad.tools.tonalanalysistools

ChordInversion
==============

.. autoclass:: ChordInversion

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
              "abjad.tools.tonalanalysistools.ChordInversion.ChordInversion" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ChordInversion</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordInversion.ChordInversion";
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

      ~abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.extent_to_figured_bass_string
      ~abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.name
      ~abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.number
      ~abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.title
      ~abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.__eq__
      ~abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.__format__
      ~abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.__hash__
      ~abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.__ne__
      ~abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.name

.. autoattribute:: abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.number

.. autoattribute:: abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.title

Methods
-------

.. automethod:: abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.extent_to_figured_bass_string

Special methods
---------------

.. automethod:: abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.__format__

.. automethod:: abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.__hash__

.. automethod:: abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.ChordInversion.ChordInversion.__repr__
