.. currentmodule:: abjad.tools.scoretools

Voice
=====

.. autoclass:: Voice

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
              "abjad.tools.scoretools.Voice.Voice" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Voice</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Context.Context";
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

      ~abjad.tools.scoretools.Voice.Voice.append
      ~abjad.tools.scoretools.Voice.Voice.consists_commands
      ~abjad.tools.scoretools.Voice.Voice.context_name
      ~abjad.tools.scoretools.Voice.Voice.extend
      ~abjad.tools.scoretools.Voice.Voice.index
      ~abjad.tools.scoretools.Voice.Voice.insert
      ~abjad.tools.scoretools.Voice.Voice.is_nonsemantic
      ~abjad.tools.scoretools.Voice.Voice.is_semantic
      ~abjad.tools.scoretools.Voice.Voice.is_simultaneous
      ~abjad.tools.scoretools.Voice.Voice.lilypond_context
      ~abjad.tools.scoretools.Voice.Voice.name
      ~abjad.tools.scoretools.Voice.Voice.pop
      ~abjad.tools.scoretools.Voice.Voice.remove
      ~abjad.tools.scoretools.Voice.Voice.remove_commands
      ~abjad.tools.scoretools.Voice.Voice.reverse
      ~abjad.tools.scoretools.Voice.Voice.select_leaves
      ~abjad.tools.scoretools.Voice.Voice.__contains__
      ~abjad.tools.scoretools.Voice.Voice.__copy__
      ~abjad.tools.scoretools.Voice.Voice.__delitem__
      ~abjad.tools.scoretools.Voice.Voice.__eq__
      ~abjad.tools.scoretools.Voice.Voice.__format__
      ~abjad.tools.scoretools.Voice.Voice.__getitem__
      ~abjad.tools.scoretools.Voice.Voice.__graph__
      ~abjad.tools.scoretools.Voice.Voice.__hash__
      ~abjad.tools.scoretools.Voice.Voice.__illustrate__
      ~abjad.tools.scoretools.Voice.Voice.__iter__
      ~abjad.tools.scoretools.Voice.Voice.__len__
      ~abjad.tools.scoretools.Voice.Voice.__mul__
      ~abjad.tools.scoretools.Voice.Voice.__ne__
      ~abjad.tools.scoretools.Voice.Voice.__repr__
      ~abjad.tools.scoretools.Voice.Voice.__rmul__
      ~abjad.tools.scoretools.Voice.Voice.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Voice.Voice.consists_commands

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Voice.Voice.is_semantic

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Voice.Voice.lilypond_context

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Voice.Voice.remove_commands

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Voice.Voice.context_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Voice.Voice.is_nonsemantic

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Voice.Voice.is_simultaneous

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Voice.Voice.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.select_leaves

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Voice.Voice.__setitem__
