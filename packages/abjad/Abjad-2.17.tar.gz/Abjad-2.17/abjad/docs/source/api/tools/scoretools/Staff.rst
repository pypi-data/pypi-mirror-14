.. currentmodule:: abjad.tools.scoretools

Staff
=====

.. autoclass:: Staff

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
              "abjad.tools.scoretools.Staff.Staff" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Staff</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Context.Context";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Staff.Staff";
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

      ~abjad.tools.scoretools.Staff.Staff.append
      ~abjad.tools.scoretools.Staff.Staff.consists_commands
      ~abjad.tools.scoretools.Staff.Staff.context_name
      ~abjad.tools.scoretools.Staff.Staff.extend
      ~abjad.tools.scoretools.Staff.Staff.index
      ~abjad.tools.scoretools.Staff.Staff.insert
      ~abjad.tools.scoretools.Staff.Staff.is_nonsemantic
      ~abjad.tools.scoretools.Staff.Staff.is_semantic
      ~abjad.tools.scoretools.Staff.Staff.is_simultaneous
      ~abjad.tools.scoretools.Staff.Staff.lilypond_context
      ~abjad.tools.scoretools.Staff.Staff.name
      ~abjad.tools.scoretools.Staff.Staff.pop
      ~abjad.tools.scoretools.Staff.Staff.remove
      ~abjad.tools.scoretools.Staff.Staff.remove_commands
      ~abjad.tools.scoretools.Staff.Staff.reverse
      ~abjad.tools.scoretools.Staff.Staff.select_leaves
      ~abjad.tools.scoretools.Staff.Staff.__contains__
      ~abjad.tools.scoretools.Staff.Staff.__copy__
      ~abjad.tools.scoretools.Staff.Staff.__delitem__
      ~abjad.tools.scoretools.Staff.Staff.__eq__
      ~abjad.tools.scoretools.Staff.Staff.__format__
      ~abjad.tools.scoretools.Staff.Staff.__getitem__
      ~abjad.tools.scoretools.Staff.Staff.__graph__
      ~abjad.tools.scoretools.Staff.Staff.__hash__
      ~abjad.tools.scoretools.Staff.Staff.__illustrate__
      ~abjad.tools.scoretools.Staff.Staff.__iter__
      ~abjad.tools.scoretools.Staff.Staff.__len__
      ~abjad.tools.scoretools.Staff.Staff.__mul__
      ~abjad.tools.scoretools.Staff.Staff.__ne__
      ~abjad.tools.scoretools.Staff.Staff.__repr__
      ~abjad.tools.scoretools.Staff.Staff.__rmul__
      ~abjad.tools.scoretools.Staff.Staff.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Staff.Staff.consists_commands

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Staff.Staff.is_semantic

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Staff.Staff.lilypond_context

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Staff.Staff.remove_commands

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Staff.Staff.context_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Staff.Staff.is_nonsemantic

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Staff.Staff.is_simultaneous

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Staff.Staff.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.select_leaves

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Staff.Staff.__setitem__
