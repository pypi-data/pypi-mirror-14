laptop-pm
---------

Use an acpi event to put the laptop in different powerstage.

usage::
 
  usage: laptop-pm [-h] [-v] [-f]  {battery,ac-adapter}


positional arguments::
   {battery,ac-adapter}  action to perform


-h      show this help message and exit
-v      make the script noisily
-f      do action even its in the same stage


To use it with an acpi event see:

- `battery <https://bitbucket.org/igraltist/kiste/src/tip/docs/examples/etc/acpi/events/battery>`_
- `ac-adapter <https://bitbucket.org/igraltist/kiste/src/tip/docs/examples/etc/acpi/events/ac-adapter>`_

You can just copy it to directory /etc/acpi/events and modify it.

To get your acpi event just call::
  
  acpi_listen
