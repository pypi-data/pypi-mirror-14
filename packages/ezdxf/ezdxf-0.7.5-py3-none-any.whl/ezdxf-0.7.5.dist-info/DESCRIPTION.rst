
ezdxf
=====

Abstract
--------

A Python package to create and modify DXF drawings, independent from the DXF
version. You can open/save every DXF file without loosing any content (except comments),
Unknown tags in the DXF file will be ignored but preserved for saving. With this behavior
it is possible to open also DXF drawings that contains data from 3rd party applications.

Quick-Info
----------

- *ezdxf* is a Python package to read and write DXF drawings
- intended audience: Developer
- requires Python 2.7 or later, runs on CPython and pypy, maybe on IronPython and Jython
- OS independent
- additional required packages: `pyparsing <https://pypi.python.org/pypi/pyparsing/2.0.1>`_
- MIT-License
- supported DXF versions read/new: R12, R2000, R2004, R2007, R2010 and R2013
- support for DXF versions R13/R14 (AC1012/AC1014), will be upgraded to R2000 (AC1015)
- support for older versions than R12, will be upgraded to R12 (AC1009)
- preserves third-party DXF content

a simple example::

    import ezdxf
    drawing = ezdxf.new(dxfversion='AC1024')  # or use the AutoCAD release name ezdxf.new(dxfversion='R2010')
    modelspace = drawing.modelspace()
    modelspace.add_line((0, 0), (10, 0), dxfattribs={'color': 7})
    drawing.layers.new('TEXTLAYER', dxfattribs={'color': 2})
    # use set_pos() for proper TEXT alignment - the relations between halign, valign, insert and align_point are tricky.
    modelspace.add_text('Test', dxfattribs={'layer': 'TEXTLAYER'}).set_pos((0, 0.2), align='CENTER')
    drawing.saveas('test.dxf')

Installation
============

Install with pip::

    pip install ezdxf

or from source::

    python setup.py install

Documentation
=============

http://pythonhosted.org/ezdxf

http://ezdxf.readthedocs.org/

The source code of ezdxf can be found on bitbucket.org at:

http://bitbucket.org/mozman/ezdxf

Feedback
========

Issue Tracker at:

https://bitbucket.org/mozman/ezdxf/issues

Feedback, Q&A, Discussions at Google Groups:

https://groups.google.com/d/forum/python-ezdxf

Mailing List:

python-ezdxf@googlegroups.com

Feedback is greatly appreciated.

Manfred

mozman@gmx.at

News
====

Version 0.7.5 - 2016-04-03

  * NEW: Drawing.acad_release property - AutoCAD release number for the drawing DXF version like 'R12' or 'R2000'
  * NEW: support for PDFUNDERLAY, DWFUNDERLAY and DGNUNDERLAY entities
  * BUGFIX: fixed broken layout setup in repair routine
  * BUGFIX: support for utf-8 encoding on saving, DXF R2007 and newer is saved with UTF-8 encoding
  * CHANGE: Drawing.add_image_def(filename, size_in_pixel, name=None), renamed key to name and set name=None for auto-generated internal image name
  * CHANGE: argument order of Layout.add_image(image_def, insert, size_in_units, rotation=0., dxfattribs=None)

Version 0.7.4 - 2016-03-13

  * NEW: support for DXF entity IMAGE (work in progress)
  * NEW: preserve leading file comments (tag code 999)
  * NEW: writes saving and upgrading comments when saving DXF files; avoid this behavior by setting options.store_comments = False
  * NEW: ezdxf.new() accepts the AutoCAD release name as DXF version string e.g. ezdxf.new('R12') or R2000, R2004, R2007, ...
  * NEW: integrated acadctb.py module from my dxfwrite package to read/write AutoCAD .ctb config files; no docs so far
  * CHANGE: renamed Drawing.groups.add() to new() for consistent name schema for adding new items to tables (public interface)
  * CHANGE: renamed Drawing.<tablename>.create() to new() for consistent name schema for adding new items to tables,
    this applies to all tables: layers, styles, dimstyles, appids, views, viewports, ucs, block_records. (public interface)
  * CHANGE: renamed Layouts.create() to new() for consistent name schema for adding new items to tables (internal interface)
  * CHANGE: renamed Drawing.create_layout() to new_layout() for consistent name schema for adding new items (public interface)
  * CHANGE: renamed factory method <layout>.add_3Dface() to add_3dface()
  * REMOVED: logging and debugging options
  * BUGFIX: fixed attribute definition for align_point in DXF entity ATTRIB (AC1015 and newer)
  * Cleanup DXF template files AC1015 - AC1027, file size goes down from >60kb to ~20kb

Version 0.7.3 - 2016-03-06

  * Quick bugfix release, because ezdxf 0.7.2 can damage DXF R12 files when saving!!!
  * NEW: improved DXF R13/R14 compatibility
  * BUGFIX: create CLASSES section only for DXF versions newer than R12 (AC1009)
  * TEST: converted a bunch of R8 (AC1003) files to R12 (AC1009), AutoCAD didn't complain
  * TEST: converted a bunch of R13 (AC1012) files to R2000 (AC1015), AutoCAD didn't complain
  * TEST: converted a bunch of R14 (AC1014) files to R2000 (AC1015), AutoCAD didn't complain

Version 0.7.2 - 2016-03-05

  * NEW: reads DXF R13/R14 and saves content as R2000 (AC1015) - experimental feature, because of the lack of test data
  * NEW: added support for common DXF attribute line weight
  * NEW: POLYLINE, POLYMESH - added properties is_closed, is_m_closed, is_n_closed
  * BUGFIX: MeshData.optimize() - corrected wrong vertex optimization
  * BUGFIX: can open DXF files without existing layout management table
  * BUGFIX: restore module structure ezdxf.const

Version 0.7.1 - 2016-02-21

  * Supported/Tested Python versions: CPython 2.7, 3.4, 3.5, pypy 4.0.1 and pypy3 2.4.0
  * NEW: read legacy DXF versions older than AC1009 (DXF R12) and saves it as DXF version AC1009.
  * NEW: added methods is_frozen(), freeze(), thaw() to class Layer()
  * NEW: full support for DXF entity ELLIPSE (added add_ellipse() method)
  * NEW: MESH data editor - implemented add_face(vertices), add_edge(vertices), optimize(precision=6) methods
  * BUGFIX: creating entities on layouts works
  * BUGFIX: entity ATTRIB - fixed halign attribute definition
  * CHANGE: POLYLINE (POLYFACE, POLYMESH) - on layer change also change layer of associated VERTEX entities

Version 0.7.0 - 2015-11-26

  * Supported Python versions: CPython 2.7, 3.4, pypy 2.6.1 and pypy3 2.4.0
  * NEW: support for DXF entity HATCH (solid fill, gradient fill and pattern fill), pattern fill with background color supported
  * NEW: support for DXF entity GROUP
  * NEW: VIEWPORT entity, but creating new viewports does not work as expected - just for reading purpose.
  * NEW: support for new common DXF attributes in AC1018 (AutoCAD 2004): true_color, color_name, transparency
  * NEW: support for new common DXF attributes in AC1021 (AutoCAD 2007): shadow_mode
  * NEW: extended custom vars interface
  * NEW: dxf2html - added support for custom properties in the header section
  * NEW: query() supports case insensitive attribute queries by appending an 'i' to the query string, e.g. '\*[layer=="construction"]i'
  * NEW: Drawing.cleanup() - call before saving the drawing but only if necessary, the process could take a while.
  * BUGFIX: query parser couldn't handle attribute names containing '_'
  * CHANGE: renamed dxf2html to pp (pretty printer), usage: py -m ezdxf.pp yourfile.dxf (generates yourfile.html in the same folder)
  * CHANGE: cleanup file structure



