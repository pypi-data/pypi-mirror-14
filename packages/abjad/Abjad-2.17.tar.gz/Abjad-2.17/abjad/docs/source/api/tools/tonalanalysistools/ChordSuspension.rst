.. currentmodule:: abjad.tools.tonalanalysistools

ChordSuspension
===============

.. autoclass:: ChordSuspension

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
              "abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ChordSuspension</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension";
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

      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.chord_name
      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.figured_bass_pair
      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.figured_bass_string
      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.is_empty
      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.start
      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.stop
      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.title_string
      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.__eq__
      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.__format__
      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.__hash__
      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.__ne__
      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.__repr__
      ~abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.chord_name

.. autoattribute:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.figured_bass_pair

.. autoattribute:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.figured_bass_string

.. autoattribute:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.is_empty

.. autoattribute:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.start

.. autoattribute:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.stop

.. autoattribute:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.title_string

Special methods
---------------

.. automethod:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.__format__

.. automethod:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.__hash__

.. automethod:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.__repr__

.. automethod:: abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension.__str__
