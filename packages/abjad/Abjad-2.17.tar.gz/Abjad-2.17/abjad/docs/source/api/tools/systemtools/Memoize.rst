.. currentmodule:: abjad.tools.systemtools

Memoize
=======

.. autoclass:: Memoize

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
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.Memoize.Memoize" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>Memoize</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.dict" [color=1,
                  group=0,
                  label=dict,
                  shape=box];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
              "builtins.object" -> "builtins.dict";
          }
          "builtins.dict" -> "abjad.tools.systemtools.Memoize.Memoize";
      }

Bases
-----

- :py:class:`builtins.dict`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.systemtools.Memoize.Memoize.clear
      ~abjad.tools.systemtools.Memoize.Memoize.copy
      ~abjad.tools.systemtools.Memoize.Memoize.get
      ~abjad.tools.systemtools.Memoize.Memoize.items
      ~abjad.tools.systemtools.Memoize.Memoize.keys
      ~abjad.tools.systemtools.Memoize.Memoize.pop
      ~abjad.tools.systemtools.Memoize.Memoize.popitem
      ~abjad.tools.systemtools.Memoize.Memoize.setdefault
      ~abjad.tools.systemtools.Memoize.Memoize.update
      ~abjad.tools.systemtools.Memoize.Memoize.values
      ~abjad.tools.systemtools.Memoize.Memoize.__call__
      ~abjad.tools.systemtools.Memoize.Memoize.__contains__
      ~abjad.tools.systemtools.Memoize.Memoize.__delitem__
      ~abjad.tools.systemtools.Memoize.Memoize.__eq__
      ~abjad.tools.systemtools.Memoize.Memoize.__ge__
      ~abjad.tools.systemtools.Memoize.Memoize.__getitem__
      ~abjad.tools.systemtools.Memoize.Memoize.__gt__
      ~abjad.tools.systemtools.Memoize.Memoize.__iter__
      ~abjad.tools.systemtools.Memoize.Memoize.__le__
      ~abjad.tools.systemtools.Memoize.Memoize.__len__
      ~abjad.tools.systemtools.Memoize.Memoize.__lt__
      ~abjad.tools.systemtools.Memoize.Memoize.__missing__
      ~abjad.tools.systemtools.Memoize.Memoize.__ne__
      ~abjad.tools.systemtools.Memoize.Memoize.__new__
      ~abjad.tools.systemtools.Memoize.Memoize.__repr__
      ~abjad.tools.systemtools.Memoize.Memoize.__setitem__

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.clear

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.get

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.items

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.keys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.popitem

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.setdefault

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.update

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.values

Special methods
---------------

.. automethod:: abjad.tools.systemtools.Memoize.Memoize.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__lt__

.. automethod:: abjad.tools.systemtools.Memoize.Memoize.__missing__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Memoize.Memoize.__setitem__
