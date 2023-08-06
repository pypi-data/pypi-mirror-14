.. currentmodule:: abjad.tools.tonalanalysistools

RomanNumeral
============

.. autoclass:: RomanNumeral

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
              "abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>RomanNumeral</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral";
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

      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.bass_scale_degree
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.extent
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.figured_bass_string
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.inversion
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.markup
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.quality
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.root_scale_degree
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.scale_degree
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.suspension
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.symbolic_string
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.__eq__
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.__format__
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.__hash__
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.__ne__
      ~abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.bass_scale_degree

.. autoattribute:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.extent

.. autoattribute:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.figured_bass_string

.. autoattribute:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.inversion

.. autoattribute:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.markup

.. autoattribute:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.quality

.. autoattribute:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.root_scale_degree

.. autoattribute:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.scale_degree

.. autoattribute:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.suspension

.. autoattribute:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.symbolic_string

Special methods
---------------

.. automethod:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.__format__

.. automethod:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.__hash__

.. automethod:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.__ne__

.. automethod:: abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral.__repr__
