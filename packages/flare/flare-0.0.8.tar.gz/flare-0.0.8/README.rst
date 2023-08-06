Flare
=====

v 0.0.8
~~~~~~~

Flare is a project initializer for Data Scientists. I built Flare to save myself time when starting a new data science project.

.. figure:: /res/directory.png
   :alt: Sample Directory Structure

   Alt text

Getting Started
~~~~~~~~~~~~~~~

Run ``pip install flare`` to get started.

Flare auto-generates a project structure for Python-based data science
exploration. It provides a directories for various transformations and
stages of data, phases of models, notebooks, and visualizations.

Virtualenvs are created for each project to keep system Python packages
undisturbed.

Run ``flare new <project-name>`` to create a new Flare project. Start
the Virtualenv with ``source venv/bin/activate``.

Utility commands for toggling the Virtualenv are underway using argparse.

License
~~~~~~~

See `license`_.

.. _license: https://github.com/francisbautista/flare/blob/master/LICENSE
