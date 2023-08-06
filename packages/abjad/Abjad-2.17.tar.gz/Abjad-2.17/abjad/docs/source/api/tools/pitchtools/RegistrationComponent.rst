.. currentmodule:: abjad.tools.pitchtools

RegistrationComponent
=====================

.. autoclass:: RegistrationComponent

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
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>RegistrationComponent</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent";
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

      ~abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.source_pitch_range
      ~abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.target_octave_start_pitch
      ~abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.__eq__
      ~abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.__format__
      ~abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.__hash__
      ~abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.__ne__
      ~abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.source_pitch_range

.. autoattribute:: abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.target_octave_start_pitch

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.__eq__

.. automethod:: abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.__format__

.. automethod:: abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent.__repr__
