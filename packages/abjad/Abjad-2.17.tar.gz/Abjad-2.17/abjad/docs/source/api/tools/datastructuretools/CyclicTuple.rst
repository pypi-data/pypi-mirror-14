.. currentmodule:: abjad.tools.datastructuretools

CyclicTuple
===========

.. autoclass:: CyclicTuple

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
              "abjad.tools.datastructuretools.CyclicTuple.CyclicTuple" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>CyclicTuple</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
              "builtins.tuple" [color=2,
                  group=1,
                  label=tuple,
                  shape=box];
              "builtins.object" -> "builtins.tuple";
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.CyclicTuple.CyclicTuple";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.tuple" -> "abjad.tools.datastructuretools.CyclicTuple.CyclicTuple";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.tuple`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.count
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.index
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__add__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__contains__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__eq__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__format__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__ge__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__getitem__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__getslice__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__gt__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__hash__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__iter__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__le__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__len__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__lt__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__mul__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__ne__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__new__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__repr__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__rmul__
      ~abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__str__

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.index

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__contains__

.. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__ge__

.. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__getitem__

.. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__getslice__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__gt__

.. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__rmul__

.. automethod:: abjad.tools.datastructuretools.CyclicTuple.CyclicTuple.__str__
