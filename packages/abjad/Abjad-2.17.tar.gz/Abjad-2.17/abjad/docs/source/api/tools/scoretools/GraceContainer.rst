.. currentmodule:: abjad.tools.scoretools

GraceContainer
==============

.. autoclass:: GraceContainer

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
              "abjad.tools.scoretools.Component.Component" [color=3,
                  group=2,
                  label=Component,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Container.Container" [color=3,
                  group=2,
                  label=Container,
                  shape=box];
              "abjad.tools.scoretools.GraceContainer.GraceContainer" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>GraceContainer</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.GraceContainer.GraceContainer";
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

      ~abjad.tools.scoretools.GraceContainer.GraceContainer.append
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.extend
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.index
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.insert
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.is_simultaneous
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.kind
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.name
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.pop
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.remove
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.reverse
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.select_leaves
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__contains__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__copy__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__delitem__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__eq__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__format__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__getitem__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__graph__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__hash__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__illustrate__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__iter__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__len__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__mul__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__ne__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__repr__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__rmul__
      ~abjad.tools.scoretools.GraceContainer.GraceContainer.__setitem__

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.GraceContainer.GraceContainer.is_simultaneous

.. autoattribute:: abjad.tools.scoretools.GraceContainer.GraceContainer.kind

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.GraceContainer.GraceContainer.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.select_leaves

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.GraceContainer.GraceContainer.__setitem__
