.. currentmodule:: abjad.tools.agenttools

PersistenceAgent
================

.. autoclass:: PersistenceAgent

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
              "abjad.tools.agenttools.PersistenceAgent.PersistenceAgent" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>PersistenceAgent</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.PersistenceAgent.PersistenceAgent";
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

      ~abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.as_ly
      ~abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.as_midi
      ~abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.as_module
      ~abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.as_pdf
      ~abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.as_png
      ~abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.client
      ~abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.__eq__
      ~abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.__format__
      ~abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.__hash__
      ~abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.__ne__
      ~abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.client

Methods
-------

.. automethod:: abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.as_ly

.. automethod:: abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.as_midi

.. automethod:: abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.as_module

.. automethod:: abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.as_pdf

.. automethod:: abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.as_png

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.PersistenceAgent.PersistenceAgent.__repr__
