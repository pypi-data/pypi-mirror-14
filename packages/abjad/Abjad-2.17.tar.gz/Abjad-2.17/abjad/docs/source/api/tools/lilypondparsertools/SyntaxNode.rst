.. currentmodule:: abjad.tools.lilypondparsertools

SyntaxNode
==========

.. autoclass:: SyntaxNode

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
          subgraph cluster_lilypondparsertools {
              graph [label=lilypondparsertools];
              "abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>SyntaxNode</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode";
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

      ~abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__eq__
      ~abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__format__
      ~abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__getitem__
      ~abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__hash__
      ~abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__len__
      ~abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__ne__
      ~abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__repr__
      ~abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__str__

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__format__

.. automethod:: abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__hash__

.. automethod:: abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__ne__

.. automethod:: abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__repr__

.. automethod:: abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode.__str__
