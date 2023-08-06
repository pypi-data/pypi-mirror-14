.. currentmodule:: abjad.tools.spannertools

Glissando
=========

.. autoclass:: Glissando

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
          subgraph cluster_spannertools {
              graph [label=spannertools];
              "abjad.tools.spannertools.Glissando.Glissando" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Glissando</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Spanner.Spanner" [color=3,
                  group=2,
                  label=Spanner,
                  shape=box];
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Glissando.Glissando";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.spannertools.Spanner.Spanner";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.spannertools.Spanner`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.spannertools.Glissando.Glissando.allow_repeated_pitches
      ~abjad.tools.spannertools.Glissando.Glissando.allow_ties
      ~abjad.tools.spannertools.Glissando.Glissando.components
      ~abjad.tools.spannertools.Glissando.Glissando.name
      ~abjad.tools.spannertools.Glissando.Glissando.overrides
      ~abjad.tools.spannertools.Glissando.Glissando.parenthesize_repeated_pitches
      ~abjad.tools.spannertools.Glissando.Glissando.__contains__
      ~abjad.tools.spannertools.Glissando.Glissando.__copy__
      ~abjad.tools.spannertools.Glissando.Glissando.__eq__
      ~abjad.tools.spannertools.Glissando.Glissando.__format__
      ~abjad.tools.spannertools.Glissando.Glissando.__getitem__
      ~abjad.tools.spannertools.Glissando.Glissando.__hash__
      ~abjad.tools.spannertools.Glissando.Glissando.__len__
      ~abjad.tools.spannertools.Glissando.Glissando.__lt__
      ~abjad.tools.spannertools.Glissando.Glissando.__ne__
      ~abjad.tools.spannertools.Glissando.Glissando.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.spannertools.Glissando.Glissando.allow_repeated_pitches

.. autoattribute:: abjad.tools.spannertools.Glissando.Glissando.allow_ties

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.Glissando.Glissando.components

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.Glissando.Glissando.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.spannertools.Glissando.Glissando.overrides

.. autoattribute:: abjad.tools.spannertools.Glissando.Glissando.parenthesize_repeated_pitches

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Glissando.Glissando.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Glissando.Glissando.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Glissando.Glissando.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Glissando.Glissando.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Glissando.Glissando.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Glissando.Glissando.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Glissando.Glissando.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Glissando.Glissando.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Glissando.Glissando.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Glissando.Glissando.__repr__
