.. currentmodule:: abjad.tools.tonalanalysistools

ChordExtent
===========

.. autoclass:: ChordExtent

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
              "abjad.tools.tonalanalysistools.ChordExtent.ChordExtent" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ChordExtent</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordExtent.ChordExtent";
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

      ~abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.name
      ~abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.number
      ~abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.__eq__
      ~abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.__format__
      ~abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.__hash__
      ~abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.__ne__
      ~abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.name

.. autoattribute:: abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.number

Special methods
---------------

.. automethod:: abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.__format__

.. automethod:: abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.__hash__

.. automethod:: abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.ChordExtent.ChordExtent.__repr__
