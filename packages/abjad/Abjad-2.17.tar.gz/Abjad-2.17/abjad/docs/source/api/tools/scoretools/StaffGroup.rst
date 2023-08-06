.. currentmodule:: abjad.tools.scoretools

StaffGroup
==========

.. autoclass:: StaffGroup

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
              "abjad.tools.scoretools.StaffGroup.StaffGroup" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>StaffGroup</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Context.Context";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.StaffGroup.StaffGroup";
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

      ~abjad.tools.scoretools.StaffGroup.StaffGroup.append
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.consists_commands
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.context_name
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.extend
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.index
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.insert
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.is_nonsemantic
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.is_semantic
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.is_simultaneous
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.lilypond_context
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.name
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.pop
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.remove
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.remove_commands
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.reverse
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.select_leaves
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__contains__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__copy__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__delitem__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__eq__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__format__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__getitem__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__graph__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__hash__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__illustrate__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__iter__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__len__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__mul__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__ne__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__repr__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__rmul__
      ~abjad.tools.scoretools.StaffGroup.StaffGroup.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.StaffGroup.StaffGroup.consists_commands

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.StaffGroup.StaffGroup.is_semantic

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.StaffGroup.StaffGroup.lilypond_context

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.StaffGroup.StaffGroup.remove_commands

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.StaffGroup.StaffGroup.context_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.StaffGroup.StaffGroup.is_nonsemantic

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.StaffGroup.StaffGroup.is_simultaneous

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.StaffGroup.StaffGroup.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.select_leaves

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.StaffGroup.StaffGroup.__setitem__
