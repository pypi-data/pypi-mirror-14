.. currentmodule:: abjad.tools.abjadbooktools

ThumbnailDirective
==================

.. autoclass:: ThumbnailDirective

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
              "abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective" [color=black,
                  fontcolor=white,
                  group=0,
                  label=<<B>ThumbnailDirective</B>>,
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
          "docutils.parsers.rst.Directive" -> "abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective";
      }

Bases
-----

- :py:class:`docutils.parsers.rst.Directive`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.add_name
      ~abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.assert_has_content
      ~abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.debug
      ~abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.directive_error
      ~abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.error
      ~abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.info
      ~abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.run
      ~abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.severe
      ~abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.warning

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.add_name

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.assert_has_content

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.debug

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.directive_error

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.error

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.info

.. automethod:: abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.run

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.severe

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective.warning
