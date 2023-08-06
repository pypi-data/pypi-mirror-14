.. currentmodule:: abjad.tools.scoretools

Context
=======

.. autoclass:: Context

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
              "abjad.tools.scoretools.Context.Context" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Context</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Score.Score" [color=3,
                  group=2,
                  label=Score,
                  shape=box];
              "abjad.tools.scoretools.Staff.Staff" [color=3,
                  group=2,
                  label=Staff,
                  shape=box];
              "abjad.tools.scoretools.StaffGroup.StaffGroup" [color=3,
                  group=2,
                  label=StaffGroup,
                  shape=box];
              "abjad.tools.scoretools.Voice.Voice" [color=3,
                  group=2,
                  label=Voice,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Context.Context";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Score.Score";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Staff.Staff";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.StaffGroup.StaffGroup";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Voice.Voice";
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

      ~abjad.tools.scoretools.Context.Context.append
      ~abjad.tools.scoretools.Context.Context.consists_commands
      ~abjad.tools.scoretools.Context.Context.context_name
      ~abjad.tools.scoretools.Context.Context.extend
      ~abjad.tools.scoretools.Context.Context.index
      ~abjad.tools.scoretools.Context.Context.insert
      ~abjad.tools.scoretools.Context.Context.is_nonsemantic
      ~abjad.tools.scoretools.Context.Context.is_semantic
      ~abjad.tools.scoretools.Context.Context.is_simultaneous
      ~abjad.tools.scoretools.Context.Context.lilypond_context
      ~abjad.tools.scoretools.Context.Context.name
      ~abjad.tools.scoretools.Context.Context.pop
      ~abjad.tools.scoretools.Context.Context.remove
      ~abjad.tools.scoretools.Context.Context.remove_commands
      ~abjad.tools.scoretools.Context.Context.reverse
      ~abjad.tools.scoretools.Context.Context.select_leaves
      ~abjad.tools.scoretools.Context.Context.__contains__
      ~abjad.tools.scoretools.Context.Context.__copy__
      ~abjad.tools.scoretools.Context.Context.__delitem__
      ~abjad.tools.scoretools.Context.Context.__eq__
      ~abjad.tools.scoretools.Context.Context.__format__
      ~abjad.tools.scoretools.Context.Context.__getitem__
      ~abjad.tools.scoretools.Context.Context.__graph__
      ~abjad.tools.scoretools.Context.Context.__hash__
      ~abjad.tools.scoretools.Context.Context.__illustrate__
      ~abjad.tools.scoretools.Context.Context.__iter__
      ~abjad.tools.scoretools.Context.Context.__len__
      ~abjad.tools.scoretools.Context.Context.__mul__
      ~abjad.tools.scoretools.Context.Context.__ne__
      ~abjad.tools.scoretools.Context.Context.__repr__
      ~abjad.tools.scoretools.Context.Context.__rmul__
      ~abjad.tools.scoretools.Context.Context.__setitem__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.scoretools.Context.Context.consists_commands

.. autoattribute:: abjad.tools.scoretools.Context.Context.is_semantic

.. autoattribute:: abjad.tools.scoretools.Context.Context.lilypond_context

.. autoattribute:: abjad.tools.scoretools.Context.Context.remove_commands

Read/write properties
---------------------

.. autoattribute:: abjad.tools.scoretools.Context.Context.context_name

.. autoattribute:: abjad.tools.scoretools.Context.Context.is_nonsemantic

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Context.Context.is_simultaneous

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Context.Context.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.select_leaves

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__ne__

.. automethod:: abjad.tools.scoretools.Context.Context.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Context.Context.__setitem__
