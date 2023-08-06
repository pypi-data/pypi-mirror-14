.. currentmodule:: abjad.tools.agenttools

MutationAgent
=============

.. autoclass:: MutationAgent

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
          subgraph cluster_agenttools {
              graph [label=agenttools];
              "abjad.tools.agenttools.MutationAgent.MutationAgent" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>MutationAgent</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=3,
                  group=2,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.MutationAgent.MutationAgent";
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

      ~abjad.tools.agenttools.MutationAgent.MutationAgent.client
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.copy
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.eject_contents
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.extract
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.fuse
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.replace
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.replace_measure_contents
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.respell_with_flats
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.respell_with_sharps
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.rewrite_meter
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.scale
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.splice
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.split
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.swap
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.transpose
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.__eq__
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.__format__
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.__hash__
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.__ne__
      ~abjad.tools.agenttools.MutationAgent.MutationAgent.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.agenttools.MutationAgent.MutationAgent.client

Methods
-------

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.copy

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.eject_contents

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.extract

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.fuse

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.replace

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.replace_measure_contents

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.respell_with_flats

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.respell_with_sharps

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.rewrite_meter

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.scale

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.splice

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.split

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.swap

.. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.transpose

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.MutationAgent.MutationAgent.__repr__
