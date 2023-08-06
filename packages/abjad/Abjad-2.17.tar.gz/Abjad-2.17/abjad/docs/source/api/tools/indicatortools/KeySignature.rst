.. currentmodule:: abjad.tools.indicatortools

KeySignature
============

.. autoclass:: KeySignature

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.KeySignature.KeySignature" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>KeySignature</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.KeySignature.KeySignature";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.indicatortools.KeySignature.KeySignature.default_scope
      ~abjad.tools.indicatortools.KeySignature.KeySignature.mode
      ~abjad.tools.indicatortools.KeySignature.KeySignature.name
      ~abjad.tools.indicatortools.KeySignature.KeySignature.tonic
      ~abjad.tools.indicatortools.KeySignature.KeySignature.__copy__
      ~abjad.tools.indicatortools.KeySignature.KeySignature.__eq__
      ~abjad.tools.indicatortools.KeySignature.KeySignature.__format__
      ~abjad.tools.indicatortools.KeySignature.KeySignature.__hash__
      ~abjad.tools.indicatortools.KeySignature.KeySignature.__ne__
      ~abjad.tools.indicatortools.KeySignature.KeySignature.__repr__
      ~abjad.tools.indicatortools.KeySignature.KeySignature.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.indicatortools.KeySignature.KeySignature.default_scope

.. autoattribute:: abjad.tools.indicatortools.KeySignature.KeySignature.mode

.. autoattribute:: abjad.tools.indicatortools.KeySignature.KeySignature.name

.. autoattribute:: abjad.tools.indicatortools.KeySignature.KeySignature.tonic

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.KeySignature.KeySignature.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.KeySignature.KeySignature.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.KeySignature.KeySignature.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.KeySignature.KeySignature.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.KeySignature.KeySignature.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.KeySignature.KeySignature.__repr__

.. automethod:: abjad.tools.indicatortools.KeySignature.KeySignature.__str__
