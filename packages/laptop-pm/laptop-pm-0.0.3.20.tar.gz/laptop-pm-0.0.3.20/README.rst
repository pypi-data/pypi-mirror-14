laptop-pm
=========

A python power mangagment scripts for a laptop which running linux.


Installation
------------

visit `installing <https://bitbucket.org/igraltist/laptop-pm/src/tip/docs/installing.rst>`_ webpage


Usage
-----

Use an acpi event to put the laptop in different powerstage.

usage::
 
  usage: laptop-pm [-h] [-v] [-f]  {battery,ac-adapter,show}


positional arguments::
   {battery,ac-adapter,show}  action to perform


-h      show this help message and exit
-v      make the script noisily
-f      do action even its in the same stage


Set device to manage:

- `example config for devices <https://bitbucket.org/igraltist/laptop-pm/src/tip/docs/examples/etc/laptop-pm/laptop-pm.json>`_

To use it with an acpi event see:

- `battery <https://bitbucket.org/igraltist/laptop-pm/src/tip/docs/examples/etc/acpi/events/battery>`_
- `ac-adapter <https://bitbucket.org/igraltist/laptop-pm/src/tip/docs/examples/etc/acpi/events/ac-adapter>`_

You can just copy it to directory /etc/acpi/events and modify it.

To get your acpi event just call::
  
  acpi_listen

You need create a file for local rc because on boot there is no acpi event.


- `startup battery check <https://bitbucket.org/igraltist/laptop-pm/src/tip/docs/examples/etc/local.d/set-power-battery.start>`_
Gentoo::

  Create /etc/local.d/set-power-battery.start and make it executable and write follow content:
        
  # check if the laptop start with battery 
  if [ "$(laptop-pm show)" = "battery" ]; then
    laptop-pm battery
  fi

  
