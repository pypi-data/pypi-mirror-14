.. currentmodule:: abjad.tools.datastructuretools

CyclicMatrix
============

.. autoclass:: CyclicMatrix

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
              "abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>CyclicMatrix</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.Matrix.Matrix" [color=3,
                  group=2,
                  label=Matrix,
                  shape=box];
              "abjad.tools.datastructuretools.Matrix.Matrix" -> "abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.Matrix.Matrix";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.Matrix`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.columns
      ~abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.rows
      ~abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.__eq__
      ~abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.__format__
      ~abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.__getitem__
      ~abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.__hash__
      ~abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.__ne__
      ~abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.columns

.. autoattribute:: abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.rows

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.__format__

.. automethod:: abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.__ne__

.. automethod:: abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix.__repr__
