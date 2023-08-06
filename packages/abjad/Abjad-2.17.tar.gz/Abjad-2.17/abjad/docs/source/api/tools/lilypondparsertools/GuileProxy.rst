.. currentmodule:: abjad.tools.lilypondparsertools

GuileProxy
==========

.. autoclass:: GuileProxy

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
              "abjad.tools.lilypondparsertools.GuileProxy.GuileProxy" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>GuileProxy</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.GuileProxy.GuileProxy";
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

      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.acciaccatura
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.appoggiatura
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.bar
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.breathe
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.clef
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.grace
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.key
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.language
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.makeClusters
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.mark
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.one_voice
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.relative
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.skip
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.slashed_grace_container
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.time
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.times
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.transpose
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.voiceFour
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.voiceOne
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.voiceThree
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.voiceTwo
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.__call__
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.__eq__
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.__format__
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.__hash__
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.__ne__
      ~abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.__repr__

Methods
-------

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.acciaccatura

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.appoggiatura

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.bar

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.breathe

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.clef

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.grace

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.key

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.language

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.makeClusters

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.mark

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.one_voice

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.relative

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.skip

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.slashed_grace_container

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.time

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.times

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.transpose

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.voiceFour

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.voiceOne

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.voiceThree

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.voiceTwo

Special methods
---------------

.. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.GuileProxy.GuileProxy.__repr__
