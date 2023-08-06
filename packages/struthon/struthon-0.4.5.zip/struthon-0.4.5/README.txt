*************************************************************************
*                                                                       *
*                              Struthon 0.4                             *
*           Structural engineering design Python applications           *
*                                                                       *
*                      (c) 2015-2016 Lukasz Laba                        *
*                                                                       *
*************************************************************************

Struthon is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Struthon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

-------------------------------------------------------------------------
* Visible changes:
-------------------------------------------------------------------------
  Struthon 0.1
  - the first working version with StruthonConcreteMonoSection application
  Struthon 0.2
  - StruthonSteelSectionBrowser application added
  Struthon 0.3.1
  - StruthonSteelSectionBrowser application upgraded (section drawing, 
    section groups filter)
  - StruthonSteelMonoSection application added
  Struthon 0.3.2
  - no changes
  Struthon 0.3.3
  - StruthonConcreteMonoSection user interface upgraded
  - StruthonConcreteMonoSection M-N chart creating speed improved
  Struthon 0.4.1
  - StruthonConcretePanel application added
  Struthon 0.4.2
  - StruthonConcretePanel upgraded
  Struthon 0.4.4
  - StruthonConcretePanel new features (dxf export, multi loadcase, save/open 
  project file)
  Struthon 0.4.2
  - StruthonConcretePanel Mecway integrated
-------------------------------------------------------------------------
* Prerequisites:
-------------------------------------------------------------------------

  Python 2.7.
  Non-standard Python library needed (tested version):
  - StruPy 0.4.6
  - Unum 4.1
  - matplotlib 1.4.2
  - PyQt4 4.11.4

  If you are beginner in Python configuration you can install Python(xy) 
  or WinPython then you only need to install strupy and unum package 
  (using "pip install strupy", and "pip install unum" in console).

-------------------------------------------------------------------------
* To install struthon:
-------------------------------------------------------------------------

  After the Python and needed library  was installed:
  On Windows use "pip install struthon" in Python shell.

  To run struthon GUI execute the file struthon.py from installed struthon
  package folder - probabiliit is "C:\Python27\Lib\site-packages\struthon"
  For easy run make shortcut on your system pulpit to this file.
  For reinstall struthon (if new version available) all you need to do is
  "pip install --upgrade struthon".
  The same do with strupy package if new version available. The created
  shortcut should be still working. 
  There is install instruction on project website.

  There may by some problem on Linux with launching aplication from struthon 
  main panel (struthon.py). You should run directly ConcreteMonoSection.py, 
  SteelMonoSection.py, SteelSectionBrowser.py etc.
   
-------------------------------------------------------------------------
* Other information :
-------------------------------------------------------------------------

  - Project website: http://struthon.org
  - E-mail : lukaszlab@o2.pl

=========================================================================
