.. currentmodule:: abjad.tools.lilypondparsertools

ContextSpeccedMusic
===================

.. autoclass:: ContextSpeccedMusic

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
          subgraph cluster_lilypondparsertools {
              graph [label=lilypondparsertools];
              "abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ContextSpeccedMusic</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.Music.Music" [color=3,
                  group=2,
                  label=Music,
                  shape=oval,
                  style=bold];
              "abjad.tools.lilypondparsertools.Music.Music" -> "abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.Music.Music";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.lilypondparsertools.Music`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.construct
      ~abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.known_contexts
      ~abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.__eq__
      ~abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.__format__
      ~abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.__hash__
      ~abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.__ne__
      ~abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.known_contexts

Methods
-------

.. automethod:: abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.construct

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic.__repr__
