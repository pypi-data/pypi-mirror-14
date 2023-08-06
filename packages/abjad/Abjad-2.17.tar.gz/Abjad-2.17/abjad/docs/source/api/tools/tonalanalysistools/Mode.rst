.. currentmodule:: abjad.tools.tonalanalysistools

Mode
====

.. autoclass:: Mode

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
              "abjad.tools.tonalanalysistools.Mode.Mode" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Mode</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.Mode.Mode";
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

      ~abjad.tools.tonalanalysistools.Mode.Mode.mode_name
      ~abjad.tools.tonalanalysistools.Mode.Mode.named_interval_segment
      ~abjad.tools.tonalanalysistools.Mode.Mode.__eq__
      ~abjad.tools.tonalanalysistools.Mode.Mode.__format__
      ~abjad.tools.tonalanalysistools.Mode.Mode.__hash__
      ~abjad.tools.tonalanalysistools.Mode.Mode.__len__
      ~abjad.tools.tonalanalysistools.Mode.Mode.__ne__
      ~abjad.tools.tonalanalysistools.Mode.Mode.__repr__
      ~abjad.tools.tonalanalysistools.Mode.Mode.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.tonalanalysistools.Mode.Mode.mode_name

.. autoattribute:: abjad.tools.tonalanalysistools.Mode.Mode.named_interval_segment

Special methods
---------------

.. automethod:: abjad.tools.tonalanalysistools.Mode.Mode.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Mode.Mode.__format__

.. automethod:: abjad.tools.tonalanalysistools.Mode.Mode.__hash__

.. automethod:: abjad.tools.tonalanalysistools.Mode.Mode.__len__

.. automethod:: abjad.tools.tonalanalysistools.Mode.Mode.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Mode.Mode.__repr__

.. automethod:: abjad.tools.tonalanalysistools.Mode.Mode.__str__
