1.6.1
=====

* Change base colours for URWID palette after complaints that the dark text
was hard to read against black backgrounds

1.6.0
=====

* Add ability for Transition to accept no code, so can do a screen wipe to
blank
* Add unit tests for Code source change methods
* Fix bugs found with above unit test

1.5.0
=====

* Changed how the wrapper to the pygments lexers work, the wrapper is now
responsible for choosing the palette to go with the colourizer, this means
custom colourizers for things that aren't code like (HTML, XML) can now have
different palettes from code
* Custom lexer now supports named palettes
* Add better error handling to the load action sequence
* Add error handling detecting Transitions that are missing both code and
code_box_to_copy
* Add error handling when trying to Replace outside of box boundaries
* Removed ReplaceTypewriter, multi-line replacement was ambiguous, use a
Remove and InsertTypewriter to explicitly do what you need
* Add error handling if a negative index is passed to InsertTypewriter,
updated incorrect documentation

1.4.0
=====

* Added methods to the Code object so you can manipulate the source before it
is rendered. You can add, remove and change lines; remove double spaces; and
if the source is python show only a subset like a given function

1.3.0
=====

* Code objects now support a custom lexer: with a little extra code you can
now use any Pygments lexer to parse your little heart out

1.2.5
=====

* hidden max_height feature was made accessible in the bin/purdy command line


1.2.4
=====

* fix bug in RTF formats where backslashes weren't escaped properly


1.2.3
=====

* moved command line scripts out of the module, it appeared to be messing up
  readthedocs, should have no impact on installation 

1.2.1
=====

* Fix bug where the compact parameter on CodeBox wasn't working
* Add parameter to SplitScreen to support the compact parameter in its top box

1.2.0
=====

* Added HighlightChain action
* Added VirtualCodeBox and ability to copy a VCB into a real code box through
  a Transition action
* Used the iscreen mechanism introduced in the last release to create a better
  test harness


1.1.1
=====

* Bug fix: purdy cmd wasn't launching properly due to type-o in fake args


1.1.0
=====

* Refactored how screens work, they're now a proxy for an implementation
  inside of "purdy.iscreen". The Urwid code viewer now lives in
  "purdy.iscreen.tui" and a new viewer has been added that does text export
* Added Sleep action
* Tranistion actions are now skippable
* Transition actions don't automatically trigger a Wait anymore, you have to
  call Wait explicitly

1.0.2
=====

* Bug fix: crash when Fold is called without a Wait immediately afterwards,
  urwid was caching a focus position and trying to set it to a line that
  wasn't there anymore

1.0.1
=====

* Bug fix: crash when fast-forward called on Transtion due to missing skip
  parameter

1.0
===

* Breaking change release
* Moved animation mechansim to be based on a queue, can now go forwards and
  backwards
* Signatures of Actions and Screens have changed
* Add tools for printing code in other formats such as RTF and HTML

0.4
===

* Add support for bash session lexer
* Add RowScreen type that can handle multiple rows and side-by-side pairs of
  boxes
* Add focus indicator to boxes without scroll indicators

0.3
===

* Added tool that uses coloured lexer to print code to console
* Added auto scrolling feature for the CodeBox containers
* Added new actions for inserting and editing lines

0.2
===

* Purdy can now be used as a library as well as a standalone script
* Added Python code lexer 
* Added scrollbar indicators
* Added SplitScreen
* Added line number support
* Added highlighting of lines


0.1.1
=====

* Patched documentation

0.1
===

* Initial release to pypi
