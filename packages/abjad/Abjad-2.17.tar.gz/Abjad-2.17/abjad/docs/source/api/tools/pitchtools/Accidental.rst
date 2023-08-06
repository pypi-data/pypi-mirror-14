.. currentmodule:: abjad.tools.pitchtools

Accidental
==========

.. autoclass:: Accidental

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
              "abjad.tools.pitchtools.Accidental.Accidental" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Accidental</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.Accidental.Accidental";
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

      ~abjad.tools.pitchtools.Accidental.Accidental.abbreviation
      ~abjad.tools.pitchtools.Accidental.Accidental.is_abbreviation
      ~abjad.tools.pitchtools.Accidental.Accidental.is_adjusted
      ~abjad.tools.pitchtools.Accidental.Accidental.is_symbolic_string
      ~abjad.tools.pitchtools.Accidental.Accidental.name
      ~abjad.tools.pitchtools.Accidental.Accidental.semitones
      ~abjad.tools.pitchtools.Accidental.Accidental.symbolic_string
      ~abjad.tools.pitchtools.Accidental.Accidental.__add__
      ~abjad.tools.pitchtools.Accidental.Accidental.__eq__
      ~abjad.tools.pitchtools.Accidental.Accidental.__format__
      ~abjad.tools.pitchtools.Accidental.Accidental.__ge__
      ~abjad.tools.pitchtools.Accidental.Accidental.__gt__
      ~abjad.tools.pitchtools.Accidental.Accidental.__hash__
      ~abjad.tools.pitchtools.Accidental.Accidental.__le__
      ~abjad.tools.pitchtools.Accidental.Accidental.__lt__
      ~abjad.tools.pitchtools.Accidental.Accidental.__ne__
      ~abjad.tools.pitchtools.Accidental.Accidental.__neg__
      ~abjad.tools.pitchtools.Accidental.Accidental.__nonzero__
      ~abjad.tools.pitchtools.Accidental.Accidental.__repr__
      ~abjad.tools.pitchtools.Accidental.Accidental.__str__
      ~abjad.tools.pitchtools.Accidental.Accidental.__sub__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.Accidental.Accidental.abbreviation

.. autoattribute:: abjad.tools.pitchtools.Accidental.Accidental.is_adjusted

.. autoattribute:: abjad.tools.pitchtools.Accidental.Accidental.name

.. autoattribute:: abjad.tools.pitchtools.Accidental.Accidental.semitones

.. autoattribute:: abjad.tools.pitchtools.Accidental.Accidental.symbolic_string

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.is_abbreviation

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.is_symbolic_string

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__add__

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__format__

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__ge__

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__gt__

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__hash__

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__le__

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__lt__

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__ne__

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__neg__

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__nonzero__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__repr__

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__str__

.. automethod:: abjad.tools.pitchtools.Accidental.Accidental.__sub__
