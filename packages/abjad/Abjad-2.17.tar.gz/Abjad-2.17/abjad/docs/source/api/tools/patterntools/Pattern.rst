.. currentmodule:: abjad.tools.patterntools

Pattern
=======

.. autoclass:: Pattern

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
          subgraph cluster_patterntools {
              graph [label=patterntools];
              "abjad.tools.patterntools.Pattern.Pattern" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Pattern</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.patterntools.Pattern.Pattern";
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

      ~abjad.tools.patterntools.Pattern.Pattern.from_vector
      ~abjad.tools.patterntools.Pattern.Pattern.get_boolean_vector
      ~abjad.tools.patterntools.Pattern.Pattern.indices
      ~abjad.tools.patterntools.Pattern.Pattern.inverted
      ~abjad.tools.patterntools.Pattern.Pattern.matches_index
      ~abjad.tools.patterntools.Pattern.Pattern.payload
      ~abjad.tools.patterntools.Pattern.Pattern.period
      ~abjad.tools.patterntools.Pattern.Pattern.reverse
      ~abjad.tools.patterntools.Pattern.Pattern.rotate
      ~abjad.tools.patterntools.Pattern.Pattern.weight
      ~abjad.tools.patterntools.Pattern.Pattern.__and__
      ~abjad.tools.patterntools.Pattern.Pattern.__copy__
      ~abjad.tools.patterntools.Pattern.Pattern.__eq__
      ~abjad.tools.patterntools.Pattern.Pattern.__format__
      ~abjad.tools.patterntools.Pattern.Pattern.__hash__
      ~abjad.tools.patterntools.Pattern.Pattern.__invert__
      ~abjad.tools.patterntools.Pattern.Pattern.__len__
      ~abjad.tools.patterntools.Pattern.Pattern.__ne__
      ~abjad.tools.patterntools.Pattern.Pattern.__or__
      ~abjad.tools.patterntools.Pattern.Pattern.__repr__
      ~abjad.tools.patterntools.Pattern.Pattern.__xor__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.patterntools.Pattern.Pattern.indices

.. autoattribute:: abjad.tools.patterntools.Pattern.Pattern.inverted

.. autoattribute:: abjad.tools.patterntools.Pattern.Pattern.payload

.. autoattribute:: abjad.tools.patterntools.Pattern.Pattern.period

.. autoattribute:: abjad.tools.patterntools.Pattern.Pattern.weight

Methods
-------

.. automethod:: abjad.tools.patterntools.Pattern.Pattern.get_boolean_vector

.. automethod:: abjad.tools.patterntools.Pattern.Pattern.matches_index

.. automethod:: abjad.tools.patterntools.Pattern.Pattern.reverse

.. automethod:: abjad.tools.patterntools.Pattern.Pattern.rotate

Class & static methods
----------------------

.. automethod:: abjad.tools.patterntools.Pattern.Pattern.from_vector

Special methods
---------------

.. automethod:: abjad.tools.patterntools.Pattern.Pattern.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.Pattern.Pattern.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.Pattern.Pattern.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.Pattern.Pattern.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.Pattern.Pattern.__hash__

.. automethod:: abjad.tools.patterntools.Pattern.Pattern.__invert__

.. automethod:: abjad.tools.patterntools.Pattern.Pattern.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.Pattern.Pattern.__ne__

.. automethod:: abjad.tools.patterntools.Pattern.Pattern.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.Pattern.Pattern.__repr__

.. automethod:: abjad.tools.patterntools.Pattern.Pattern.__xor__
