.. currentmodule:: abjad.tools.abjadbooktools

AbjadDirective
==============

.. autoclass:: AbjadDirective

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
          subgraph cluster_abjadbooktools {
              graph [label=abjadbooktools];
              "abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective" [color=black,
                  fontcolor=white,
                  group=0,
                  label=<<B>AbjadDirective</B>>,
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
          subgraph cluster_docutils {
              graph [label=docutils];
              "docutils.parsers.rst.Directive" [color=3,
                  group=2,
                  label=Directive,
                  shape=box];
          }
          "builtins.object" -> "docutils.parsers.rst.Directive";
          "docutils.parsers.rst.Directive" -> "abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective";
      }

Bases
-----

- :py:class:`docutils.parsers.rst.Directive`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.add_name
      ~abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.assert_has_content
      ~abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.debug
      ~abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.directive_error
      ~abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.error
      ~abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.info
      ~abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.run
      ~abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.severe
      ~abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.warning

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.add_name

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.assert_has_content

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.debug

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.directive_error

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.error

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.info

.. automethod:: abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.run

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.severe

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective.warning
