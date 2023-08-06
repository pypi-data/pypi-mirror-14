.. currentmodule:: abjad.tools.scoretools

Cluster
=======

.. autoclass:: Cluster

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
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.Cluster.Cluster" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Cluster</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Component.Component" [color=3,
                  group=2,
                  label=Component,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Container.Container" [color=3,
                  group=2,
                  label=Container,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Cluster.Cluster";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.Component.Component";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.scoretools.Container`

- :py:class:`abjad.tools.scoretools.Component`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.Cluster.Cluster.append
      ~abjad.tools.scoretools.Cluster.Cluster.extend
      ~abjad.tools.scoretools.Cluster.Cluster.index
      ~abjad.tools.scoretools.Cluster.Cluster.insert
      ~abjad.tools.scoretools.Cluster.Cluster.is_simultaneous
      ~abjad.tools.scoretools.Cluster.Cluster.name
      ~abjad.tools.scoretools.Cluster.Cluster.pop
      ~abjad.tools.scoretools.Cluster.Cluster.remove
      ~abjad.tools.scoretools.Cluster.Cluster.reverse
      ~abjad.tools.scoretools.Cluster.Cluster.select_leaves
      ~abjad.tools.scoretools.Cluster.Cluster.__contains__
      ~abjad.tools.scoretools.Cluster.Cluster.__copy__
      ~abjad.tools.scoretools.Cluster.Cluster.__delitem__
      ~abjad.tools.scoretools.Cluster.Cluster.__eq__
      ~abjad.tools.scoretools.Cluster.Cluster.__format__
      ~abjad.tools.scoretools.Cluster.Cluster.__getitem__
      ~abjad.tools.scoretools.Cluster.Cluster.__graph__
      ~abjad.tools.scoretools.Cluster.Cluster.__hash__
      ~abjad.tools.scoretools.Cluster.Cluster.__illustrate__
      ~abjad.tools.scoretools.Cluster.Cluster.__iter__
      ~abjad.tools.scoretools.Cluster.Cluster.__len__
      ~abjad.tools.scoretools.Cluster.Cluster.__mul__
      ~abjad.tools.scoretools.Cluster.Cluster.__ne__
      ~abjad.tools.scoretools.Cluster.Cluster.__repr__
      ~abjad.tools.scoretools.Cluster.Cluster.__rmul__
      ~abjad.tools.scoretools.Cluster.Cluster.__setitem__

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Cluster.Cluster.is_simultaneous

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Cluster.Cluster.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.select_leaves

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Cluster.Cluster.__setitem__
