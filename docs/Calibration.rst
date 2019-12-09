.. _Calibration:

===========
Calibration
===========

For the calibration you can run:

.. code-block:: bash

  ./puffyCV.py cal <camera-id>

Be sure to calibrate one camera at a time. To find out which camera IDs are recognised by your host system just run the shell-script included in the root directory:

.. code-block:: bash

  ./enumerate_cams.sh

  ██████╗ ██╗   ██╗███████╗███████╗██╗   ██╗ ██████╗██╗   ██╗
  ██╔══██╗██║   ██║██╔════╝██╔════╝╚██╗ ██╔╝██╔════╝██║   ██║   by Patrick Hener
  ██████╔╝██║   ██║█████╗  █████╗   ╚████╔╝ ██║     ██║   ██║   patrickhener@gmx.de
  ██╔═══╝ ██║   ██║██╔══╝  ██╔══╝    ╚██╔╝  ██║     ╚██╗ ██╔╝   Version: 0.9, 2019-2020
  ██║     ╚██████╔╝██║     ██║        ██║   ╚██████╗ ╚████╔╝    http://puffycv.rtfd.io/
  ╚═╝      ╚═════╝ ╚═╝     ╚═╝        ╚═╝    ╚═════╝  ╚═══╝
  
  
  I 2019-12-09 14:55:38 Video Device with ID 0 is an accessible camera
  E 2019-12-09 14:55:38 Video Device with ID 1 is not an accessible camera
  I 2019-12-09 14:55:38 Video Device with ID 2 is an accessible camera
  E 2019-12-09 14:55:38 Video Device with ID 3 is not an accessible camera
  I 2019-12-09 14:55:38 Video Device with ID 4 is an accessible camera
  E 2019-12-09 14:55:38 Video Device with ID 5 is not an accessible camera
  E 2019-12-09 14:55:38 Video Device with ID 6 is not an accessible camera
  E 2019-12-09 14:55:38 Video Device with ID 7 is not an accessible camera
  E 2019-12-09 14:55:38 Video Device with ID 8 is not an accessible camera
  E 2019-12-09 14:55:38 Video Device with ID 9 is not an accessible camera

Settings
--------
