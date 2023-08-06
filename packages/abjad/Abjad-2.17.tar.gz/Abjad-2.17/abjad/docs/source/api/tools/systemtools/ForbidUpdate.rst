.. currentmodule:: abjad.tools.systemtools

ForbidUpdate
============

.. autoclass:: ForbidUpdate

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
              "abjad.tools.abctools.ContextManager.ContextManager" [color=1,
                  group=0,
                  label=ContextManager,
                  shape=oval,
                  style=bold];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.ContextManager.ContextManager";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.ForbidUpdate.ForbidUpdate" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ForbidUpdate</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.ForbidUpdate.ForbidUpdate";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.ContextManager`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.component
      ~abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.update_on_enter
      ~abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.update_on_exit
      ~abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__enter__
      ~abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__eq__
      ~abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__exit__
      ~abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__format__
      ~abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__hash__
      ~abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__ne__
      ~abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.component

.. autoattribute:: abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.update_on_enter

.. autoattribute:: abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.update_on_exit

Special methods
---------------

.. automethod:: abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__enter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__eq__

.. automethod:: abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__exit__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ForbidUpdate.ForbidUpdate.__repr__
