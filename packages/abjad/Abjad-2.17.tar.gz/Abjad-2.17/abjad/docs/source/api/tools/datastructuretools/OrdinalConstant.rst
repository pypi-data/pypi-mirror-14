.. currentmodule:: abjad.tools.datastructuretools

OrdinalConstant
===============

.. autoclass:: OrdinalConstant

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
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>OrdinalConstant</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant";
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

      ~abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__eq__
      ~abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__format__
      ~abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__ge__
      ~abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__gt__
      ~abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__hash__
      ~abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__le__
      ~abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__lt__
      ~abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__ne__
      ~abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__new__
      ~abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__repr__

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__eq__

.. automethod:: abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__format__

.. automethod:: abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__ge__

.. automethod:: abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__gt__

.. automethod:: abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__hash__

.. automethod:: abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__le__

.. automethod:: abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__ne__

.. automethod:: abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__new__

.. automethod:: abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant.__repr__
