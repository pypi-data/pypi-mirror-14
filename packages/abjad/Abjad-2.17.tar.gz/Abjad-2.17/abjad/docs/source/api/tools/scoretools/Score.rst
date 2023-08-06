.. currentmodule:: abjad.tools.scoretools

Score
=====

.. autoclass:: Score

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
              "abjad.tools.scoretools.Context.Context" [color=3,
                  group=2,
                  label=Context,
                  shape=box];
              "abjad.tools.scoretools.Score.Score" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Score</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Context.Context";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Score.Score";
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

- :py:class:`abjad.tools.scoretools.Context`

- :py:class:`abjad.tools.scoretools.Container`

- :py:class:`abjad.tools.scoretools.Component`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.Score.Score.add_final_bar_line
      ~abjad.tools.scoretools.Score.Score.add_final_markup
      ~abjad.tools.scoretools.Score.Score.append
      ~abjad.tools.scoretools.Score.Score.consists_commands
      ~abjad.tools.scoretools.Score.Score.context_name
      ~abjad.tools.scoretools.Score.Score.extend
      ~abjad.tools.scoretools.Score.Score.index
      ~abjad.tools.scoretools.Score.Score.insert
      ~abjad.tools.scoretools.Score.Score.is_nonsemantic
      ~abjad.tools.scoretools.Score.Score.is_semantic
      ~abjad.tools.scoretools.Score.Score.is_simultaneous
      ~abjad.tools.scoretools.Score.Score.lilypond_context
      ~abjad.tools.scoretools.Score.Score.name
      ~abjad.tools.scoretools.Score.Score.pop
      ~abjad.tools.scoretools.Score.Score.remove
      ~abjad.tools.scoretools.Score.Score.remove_commands
      ~abjad.tools.scoretools.Score.Score.reverse
      ~abjad.tools.scoretools.Score.Score.select_leaves
      ~abjad.tools.scoretools.Score.Score.__contains__
      ~abjad.tools.scoretools.Score.Score.__copy__
      ~abjad.tools.scoretools.Score.Score.__delitem__
      ~abjad.tools.scoretools.Score.Score.__eq__
      ~abjad.tools.scoretools.Score.Score.__format__
      ~abjad.tools.scoretools.Score.Score.__getitem__
      ~abjad.tools.scoretools.Score.Score.__graph__
      ~abjad.tools.scoretools.Score.Score.__hash__
      ~abjad.tools.scoretools.Score.Score.__illustrate__
      ~abjad.tools.scoretools.Score.Score.__iter__
      ~abjad.tools.scoretools.Score.Score.__len__
      ~abjad.tools.scoretools.Score.Score.__mul__
      ~abjad.tools.scoretools.Score.Score.__ne__
      ~abjad.tools.scoretools.Score.Score.__repr__
      ~abjad.tools.scoretools.Score.Score.__rmul__
      ~abjad.tools.scoretools.Score.Score.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Score.Score.consists_commands

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Score.Score.is_semantic

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Score.Score.lilypond_context

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Score.Score.remove_commands

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Score.Score.context_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Score.Score.is_nonsemantic

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Score.Score.is_simultaneous

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Score.Score.name

Methods
-------

.. automethod:: abjad.tools.scoretools.Score.Score.add_final_bar_line

.. automethod:: abjad.tools.scoretools.Score.Score.add_final_markup

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.select_leaves

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Score.Score.__setitem__
