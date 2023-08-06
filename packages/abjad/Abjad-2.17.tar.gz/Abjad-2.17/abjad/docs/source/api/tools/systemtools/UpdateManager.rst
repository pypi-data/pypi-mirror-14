.. currentmodule:: abjad.tools.systemtools

UpdateManager
=============

.. autoclass:: UpdateManager

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
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.UpdateManager.UpdateManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>UpdateManager</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.UpdateManager.UpdateManager";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.systemtools.UpdateManager.UpdateManager.__eq__
      ~abjad.tools.systemtools.UpdateManager.UpdateManager.__format__
      ~abjad.tools.systemtools.UpdateManager.UpdateManager.__hash__
      ~abjad.tools.systemtools.UpdateManager.UpdateManager.__ne__
      ~abjad.tools.systemtools.UpdateManager.UpdateManager.__repr__

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.UpdateManager.UpdateManager.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.UpdateManager.UpdateManager.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.UpdateManager.UpdateManager.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.UpdateManager.UpdateManager.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.UpdateManager.UpdateManager.__repr__
