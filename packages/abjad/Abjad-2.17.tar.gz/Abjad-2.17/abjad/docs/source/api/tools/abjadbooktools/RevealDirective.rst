.. currentmodule:: abjad.tools.abjadbooktools

RevealDirective
===============

.. autoclass:: RevealDirective

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
              "abjad.tools.abjadbooktools.RevealDirective.RevealDirective" [color=black,
                  fontcolor=white,
                  group=0,
                  label=<<B>RevealDirective</B>>,
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
          "docutils.parsers.rst.Directive" -> "abjad.tools.abjadbooktools.RevealDirective.RevealDirective";
      }

Bases
-----

- :py:class:`docutils.parsers.rst.Directive`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.abjadbooktools.RevealDirective.RevealDirective.add_name
      ~abjad.tools.abjadbooktools.RevealDirective.RevealDirective.assert_has_content
      ~abjad.tools.abjadbooktools.RevealDirective.RevealDirective.debug
      ~abjad.tools.abjadbooktools.RevealDirective.RevealDirective.directive_error
      ~abjad.tools.abjadbooktools.RevealDirective.RevealDirective.error
      ~abjad.tools.abjadbooktools.RevealDirective.RevealDirective.info
      ~abjad.tools.abjadbooktools.RevealDirective.RevealDirective.run
      ~abjad.tools.abjadbooktools.RevealDirective.RevealDirective.severe
      ~abjad.tools.abjadbooktools.RevealDirective.RevealDirective.warning

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.RevealDirective.RevealDirective.add_name

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.RevealDirective.RevealDirective.assert_has_content

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.RevealDirective.RevealDirective.debug

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.RevealDirective.RevealDirective.directive_error

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.RevealDirective.RevealDirective.error

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.RevealDirective.RevealDirective.info

.. automethod:: abjad.tools.abjadbooktools.RevealDirective.RevealDirective.run

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.RevealDirective.RevealDirective.severe

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.RevealDirective.RevealDirective.warning
