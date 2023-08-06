.. currentmodule:: abjad.tools.scoretools

Skip
====

.. autoclass:: Skip

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
              "abjad.tools.scoretools.Leaf.Leaf" [color=3,
                  group=2,
                  label=Leaf,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Skip.Skip" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Skip</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Leaf.Leaf";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Skip.Skip";
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

- :py:class:`abjad.tools.scoretools.Leaf`

- :py:class:`abjad.tools.scoretools.Component`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.Skip.Skip.name
      ~abjad.tools.scoretools.Skip.Skip.written_duration
      ~abjad.tools.scoretools.Skip.Skip.__copy__
      ~abjad.tools.scoretools.Skip.Skip.__eq__
      ~abjad.tools.scoretools.Skip.Skip.__format__
      ~abjad.tools.scoretools.Skip.Skip.__hash__
      ~abjad.tools.scoretools.Skip.Skip.__illustrate__
      ~abjad.tools.scoretools.Skip.Skip.__mul__
      ~abjad.tools.scoretools.Skip.Skip.__ne__
      ~abjad.tools.scoretools.Skip.Skip.__repr__
      ~abjad.tools.scoretools.Skip.Skip.__rmul__
      ~abjad.tools.scoretools.Skip.Skip.__str__

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Skip.Skip.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Skip.Skip.written_duration

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Skip.Skip.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Skip.Skip.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Skip.Skip.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Skip.Skip.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Skip.Skip.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Skip.Skip.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Skip.Skip.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Skip.Skip.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Skip.Skip.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Skip.Skip.__str__
