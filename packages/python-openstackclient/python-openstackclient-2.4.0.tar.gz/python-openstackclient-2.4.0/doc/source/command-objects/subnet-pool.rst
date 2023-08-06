===========
subnet pool
===========

Network v2

subnet pool create
------------------

Create subnet pool

.. program:: subnet pool create
.. code:: bash

    os subnet pool create
        [--pool-prefix <pool-prefix> [...]]
        [--default-prefix-length <default-prefix-length>]
        [--min-prefix-length <min-prefix-length>]
        [--max-prefix-length <max-prefix-length>]
        [--project <project> [--project-domain <project-domain>]]
        [--address-scope <address-scope>]
        <name>

.. option:: --pool-prefix <pool-prefix>

    Set subnet pool prefixes (in CIDR notation)
    (repeat option to set multiple prefixes)

.. option:: --default-prefix-length <default-prefix-length>

    Set subnet pool default prefix length

.. option:: --min-prefix-length <min-prefix-length>

    Set subnet pool minimum prefix length

.. option:: --max-prefix-length <max-prefix-length>

    Set subnet pool maximum prefix length

.. option:: --project <project>

    Owner's project (name or ID)

.. option:: --project-domain <project-domain>

    Domain the project belongs to (name or ID). This can be used in case
    collisions between project names exist.

.. option:: --address-scope <address-scope>

    Set address scope associated with the subnet pool (name or ID),
    prefixes must be unique across address scopes

.. _subnet_pool_create-name:
.. describe:: <name>

    Name of the new subnet pool

subnet pool delete
------------------

Delete subnet pool

.. program:: subnet pool delete
.. code:: bash

    os subnet pool delete
        <subnet-pool>

.. _subnet_pool_delete-subnet-pool:
.. describe:: <subnet-pool>

    Subnet pool to delete (name or ID)

subnet pool list
----------------

List subnet pools

.. program:: subnet pool list
.. code:: bash

    os subnet pool list
        [--long]

.. option:: --long

    List additional fields in output

subnet pool set
---------------

Set subnet pool properties

.. program:: subnet pool set
.. code:: bash

    os subnet pool set
        [--name <name>]
        [--pool-prefix <pool-prefix> [...]]
        [--default-prefix-length <default-prefix-length>]
        [--min-prefix-length <min-prefix-length>]
        [--max-prefix-length <max-prefix-length>]
        [--address-scope <address-scope> | --no-address-scope]
        <subnet-pool>

.. option:: --name <name>

    Set subnet pool name

.. option:: --pool-prefix <pool-prefix>

    Set subnet pool prefixes (in CIDR notation)
    (repeat option to set multiple prefixes)

.. option:: --default-prefix-length <default-prefix-length>

    Set subnet pool default prefix length

.. option:: --min-prefix-length <min-prefix-length>

    Set subnet pool minimum prefix length

.. option:: --max-prefix-length <max-prefix-length>

    Set subnet pool maximum prefix length

.. option:: --address-scope <address-scope>

    Set address scope associated with the subnet pool (name or ID),
    prefixes must be unique across address scopes

.. option:: --no-address-scope

    Remove address scope associated with the subnet pool

.. _subnet_pool_set-subnet-pool:
.. describe:: <subnet-pool>

    Subnet pool to modify (name or ID)

subnet pool show
----------------

Display subnet pool details

.. program:: subnet pool show
.. code:: bash

    os subnet pool show
        <subnet-pool>

.. _subnet_pool_show-subnet-pool:
.. describe:: <subnet-pool>

    Subnet pool to display (name or ID)
