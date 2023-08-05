HitchSystem
===========

System handler for hitchtest. This package handles the installation
of required system packages for hitch projects, either via apt-get, yum,
pacman or brew.


Use
===

To use::

  $ hitch system install
  [ attempts installation of system packages ]

  $ hitch system freeze
  [ prints packages required by the system ]
