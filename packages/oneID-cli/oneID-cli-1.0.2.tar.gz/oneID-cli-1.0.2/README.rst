oneID CLI
=========

|CIStatus|_

.. |CIStatus| image:: https://circleci.com/gh/OneID/oneid-cli.svg?style=shield&circle-token=053ccef5cf83b6254701ab381fe9baf58d28670e
.. _CIStatus: https://circleci.com/gh/OneID/oneid-cli

Install oneID Command Line Interface

.. code-block:: console

    pip install oneid-cli


Configure your computer (requires your oneID UUID & Secret Key)

.. code-block:: console

    oneid-cli configure


Create a new Project

.. code-block:: console

    oneid-cli create-project --name "My New Project"



List all your Projects

.. code-block:: console

    oneid-cli list-projects



List details for a Project

.. code-block:: console

    oneid-cli list-projects --project <project-uuid>



Provision a new IoT Device

.. code-block:: console

    oneid-cli provision --type edge_device --name "My IoT Device" --project <project-uuid>



Provision a new Server

.. code-block::

    oneid-cli provision --type server --name "My Server" --project <project-uuid>


To send messages between devices and servers, use `oneID-connect`, available at `<http://oneid-connect.readthedocs.org/en/latest/>`_
