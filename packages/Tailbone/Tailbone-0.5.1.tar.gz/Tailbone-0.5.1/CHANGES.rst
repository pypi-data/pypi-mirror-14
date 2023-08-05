
CHANGELOG
=========

0.5.1 (2016-02-27)
------------------

* Fix bug when rendering email bounce links.


0.5.0 (2016-02-15)
------------------

* Refactor products view(s) per new master pattern.

* Make our ``DateTimeFieldRenderer`` the default for datetime fields.

* Add new ``BatchMasterView`` for new-style batches.

* Overhaul vendor catalogs, vendor invoices views to use new batch master class.

* Refactor some more model views to use MasterView. (depositlink, tax, emailbounce)

* Make datasync views easier to customize.


0.4.42
------

* Add initial reply / reply-all support for messages.

* Add subscriber hook for setting inbox count in template context.


0.4.41
------

* Tweak how we connect a user to a batch, when refreshing.

* Add 'Move' button to message view template.


0.4.40
------

* Make rattail config object use our scoped session, when consulting db.


0.4.39
------

* Add support for sending new messages.


0.4.38
------

* Add 'password is/not null' filter to users list view.

* Remove style hack for message grid views.


0.4.37
------

* Add 'messages.list' permission, to protect inbox etc.


0.4.36
------

* Fix bug when marking batch as executed.


0.4.35
------

* Change default form buttons so Cancel is also a button.

* Add 'Stores' and 'Departments' fields to Employee fieldset.


0.4.34
------

* Add 'restart datasync' button to datasync changes list page.

* Add autocomplete vendor field renderer.

* Change vendor catalog upload, to allow vendor-less parsers.

* Stop depending on PIL...for now?


0.4.33
------

* Add employee/department relationships to employee and department views.


0.4.32
------

* Add edit mode for email "profile" settings.

* Fix auto-creation of grid sorter, when joined table is involved.

* Add initial support for 'messages' views.


0.4.31
------

* Add speed bump / confirmation page when deleting records.

* Add "grid tools" to "complete" grid template.

* Add ``Person.middle_name`` to the fieldset.


0.4.30
------

* Add config extension, to record data changes if so configured.

* Add mailing address to person fieldset.


0.4.29
------

* Fix some route names.


0.4.28
------

* Use sample data when generating subject for display in email profile settings.

* Convert (most?) basic views to use master view pattern.


0.4.27
------

* Change default sortkey for email profiles list.

* Add 'To' field to email profile settings grid.


0.4.26
------

* Add readonly support for email profile settings.


0.4.25
------

* Fix bug when 'edbob.permissions' setting is empty.

* Tweak some things to get Tailbone working on its own.

* Let subclass of MasterView override the database Session it uses.


0.4.24
------

* Render ``DataSyncChange.obtained`` as humanized timestamp within UI.


0.4.23
------

* Delete product costs for vendor when deleting vendor.

* Work around formalchemy config bug, caused by edbob.

* Add view to show DataSync changes, for basic troubleshooting.


0.4.22
------

* Remove format hack which isn't py2.6-friendly.


0.4.21
------

* Add "valueless verbs" concept to grid filters.

* Tweak labels for new grid filter form buttons.

* Configure logging when starting up.

* Add HTML5 doctype to base template.

* More grid filter improvements; add choice/enum/date value renderers.

* Treat filter by "contains X Y" as "contains X and contains Y".

* Tweak layout CSS so page body expands to fill screen.


0.4.20
------

* Add ``CurrencyFieldRenderer``.

* Add basic checkbox support to new grids.

* Add 'Default Filters' and 'Clear Filters' buttons to new grid filters form.

* Add "Save Defaults" button so user can save personal defaults for any new grid.

* Fix bug when rendering hidden field in FA fieldset.

* Remove some unused styles.

* Various tweaks to support "late login" idea when uploading new batch.

* Hard-code old grid pagecount settings, to avoid ``edbob.config``.

* Refactor app configuration to use ``rattail.config.make_config()``.

* Tweak label formatter instantiation, per rattail changes.

* Various tweaks to base batch views.

* Add ``CustomFieldRenderer`` and ``DateFieldRenderer``.

* Add ``configure_fieldset()`` stub for master view.

* Add progress indicator to batch execution.

* Add ability to download batch row data as CSV.


0.4.19
------

* Fix progress template, per jQuery CDN changes.


0.4.18
------

* Don't show flash message when user logs in.

* Add core JS/CSS to base template; use CDN instead of cached files.

* Add support for "new-style grids" and "model master views", and convert the
  following views to use it: roles, users, label profiles, settings.  Also
  overhaul how permissions are registered in app config.


0.4.17
------

* Log warning instead of error when refreshing batch fails.


0.4.16
------

* Add initial support for email bounce management.


0.4.15
------

* Fix missing import bug.


0.4.14
------

* Make anchor tags with 'button' class render as jQuery UI buttons.

* Tweak ``app.make_rattail_config()`` to allow caller to define some settings.

* Add ``display_name`` field to employee CRUD view.

* Allow batch handler to disable the Execute button.

* Add ``StoreFieldRenderer`` and ``DecimalFieldRenderer``.

* Tweak how default filter config is handled for batch grid views.

* Add list of assigned users to role view page.

* Add products autocomplete view.

* Add ``rattail_config`` attribute to base ``View`` class.

* Fix timezone issues with ``util.pretty_datetime()`` function.

* Add some custom FormEncode validators.


0.4.13
------

* Fix query bugs for batch row grid views (add join support).

* Make vendor field renderer show ID in readonly mode.

* Change permission requirement for refreshing a batch's data.

* Add flash message when any batch executes successfully.

* Add autocomplete view for current employees.

* Add autocomplete employee field renderer.

* Fix usage of ``Product.unit_of_measure`` vs. ``Product.weighed``.


0.4.12
------

* Fix bug when creating batch from product query.


0.4.11
------

* Tweak old-style batch execution call.


0.4.10
------

* Add 'fake_error' view to test exception handling.

* Add ability to view details (i.e. all fields) of a batch row.

* Fix bulk delete of batch rows, to set 'removed' flag instead.

* Fix vendor invoice validation bug.

* Add dept. number and friends to product details page.

* Add "extra panels" customization hook to product details template.


0.4.9
-----

* Hide "print labels" column on products list view if so configured.


0.4.8
-----

* Fix permission for deposit link list/search view.

* Fix permission for taxes list/search view.


0.4.7
-----

* Add views for deposit links, taxes; update product view.

* Add some new vendor and product fields.

* Add panels to product details view, etc.

* Fix login so user is sent to their target page after authentication.

* Don't allow edit of vendor and effective date in catalog batches.

* Add shared GPC search filter, use it for product batch rows.

* Add default ``Grid.iter_rows()`` implementation.

* Add "save" icon and grid column style.

* Add ``numeric.js`` script for numeric-only text inputs.

* Add product UPC to JSON output of 'products.search' view.


0.4.6
-----

* Add vendor catalog batch importer.

* Add vendor invoice batch importer.

* Improve data file handling for file batches.

* Add download feature for file batches.

* Add better error handling when batch refresh fails, etc.

* Add some docs for new batch system.

* Refactor ``app`` module to promote code sharing.

* Force grid table background to white.

* Exclude 'deleted' items from reports.

* Hide deleted field from product details, according to permissions.

* Fix embedded grid URL query string bug.


0.4.5
-----

* Add prettier UPCs to ordering worksheet report.

* Add case pack field to product CRUD form.


0.4.4
-----

* Add UI support for ``Product.deleted`` column.


0.4.3
-----

* More versioning support fixes, to allow on or off.


0.4.2
-----

* Rework versioning support to allow it to be on or off.


0.4.1
-----

* Only attempt to count versions for versioned models (CRUD views).


0.4.0
-----

This version primarily got the bump it did because of the addition of support
for SQLAlchemy-Continuum versioning.  There were several other minor changes as
well.

* Add department to field lists for category views.

* Change default sort for People grid view.

* Add category to product CRUD view.

* Add initial versioning support with SQLAlchemy-Continuum.


0.3.28
------

* Add unique username check when creating users.

* Improve UPC search for rows within batches.

* New batch system...


0.3.27
------

* Fix bug with default search filters for SA grids.

* Fix bug in product search UPC filter.

* Ugh, add unwanted jQuery libs to progress template.

* Add support for integer search filters.


0.3.26
------

* Use boolean search filter for batch column filters of 'FLAG' type.


0.3.25
------

* Make product UPC search view strip non-digit chars from input.


0.3.24
------

* Make ``GPCFieldRenderer`` display check digit separate from main barcode
  data.

* Add ``DateTimeFieldRenderer`` to show human-friendly timestamps.

* Tweak CRUD form buttons a little.

* Add grid, CRUD views for ``Setting`` model.

* Update ``base.css`` with various things from other projects.

* Fix bug with progress template, when error occurs.


0.3.23
------

* Fix bugs when configuring database session within threads.


0.3.22
------

* Make ``Store.database_key`` field editable.

* Add explicit session config within batch threads.

* Remove cap on installed Pyramid version.

* Change session progress API.


0.3.21
------

* Add monospace font for label printer format command.


0.3.20
------

* Refactor some label printing stuff, per rattail changes.


0.3.19
------

* Add support for ``Product.not_for_sale`` flag.


0.3.18
------

* Add explicit file encoding to all Mako templates.

* Add "active" filter to users view; enable it by default.


0.3.17
------

* Add customer phone autocomplete and customer "info" AJAX view.

* Allow editing ``User.active`` field.

* Add Person autocomplete view which restricts to employees only.


0.3.16
------

* Add product report codes to the UI.


0.3.15
------

* Add experimental soundex filter support to the Customers grid.


0.3.14
------

* Add event hook for attaching Rattail ``config`` to new requests.

* Fix vendor filter/sort issues in products grid.

* Add ``Family`` and ``Product.family`` to the general grid/crud UI.

* Add POD image support to product view page.


0.3.13
------

* Use global ``Session`` from rattail (again).

* Apply zope transaction to global Tailbone Session class.


0.3.12
------

* Fix customer lookup bug in customer detail view.

* Add ``SessionProgress`` class, and ``progress`` views.


0.3.11
------

* Removed reliance on global ``rattail.db.Session`` class.


0.3.10
------

* Changed ``UserFieldRenderer`` to leverage ``User.display_name``.

* Refactored model imports, etc.
    
  This is in preparation for using database models only from ``rattail``
  (i.e. no ``edbob``).  Mostly the model and enum imports were affected.

* Removed references to ``edbob.enum``.


0.3.9
-----

* Added forbidden view.

* Fixed bug with ``request.has_any_perm()``.

* Made ``SortableAlchemyGridView`` default to full (100%) width.

* Refactored ``AutocompleteFieldRenderer``.
    
  Also improved some organization of renderers.

* Allow overriding form class/factory for CRUD views.

* Made ``EnumFieldRenderer`` a proper class.

* Don't sort values in ``EnumFieldRenderer``.
    
  The dictionaries used to supply enumeration values should be ``OrderedDict``
  instances if sorting is needed.

* Added ``Product.family`` to CRUD view.


0.3.8
-----

* Fixed manifest (whoops).


0.3.7
-----

* Added some autocomplete Javascript magic.
    
  Not sure how this got missed the first time around.

* Added ``products.search`` route/view.
    
  This is for simple AJAX uses.

* Fixed grid join map bug.


0.3.6
-----

* Fixed change password template/form.


0.3.5
-----

* Added ``forms.alchemy`` module and changed CRUD view to use it.

* Added progress template.


0.3.4
-----

* Changed vendor filter in product search to find "any vendor".
    
  I.e. the current filter is *not* restricted to the preferred vendor only.
  Probably should still add one (back) for preferred only as well; hence the
  commented code.


0.3.3
-----

* Major overhaul for standalone operation.
    
  This removes some of the ``edbob`` reliance, as well as borrowing some
  templates and styling etc. from Dtail.

  Stop using ``edbob.db.engine``, stop using all edbob templates, etc.

* Fix authorization policy bug.
    
  This was really an edge case, but in any event the problem would occur when a
  user was logged in, and then that user account was deleted.

* Added ``global_title()`` to base template.

* Made logo more easily customizable in login template.


0.3.2
-----

* Rebranded to Tailbone.


0.3.1
-----

* Added some tests.

* Added ``helpers`` module.
    
  Also added a Pyramid subscriber hook to add the module to the template
  renderer context with a key of ``h``.  This is nothing really new, but it
  overrides the helper provided by ``edbob``, and adds a ``pretty_date()``
  function (which maybe isn't a good idea anyway..?).

* Added ``simpleform`` wildcard import to ``forms`` module.

* Added autocomplete view and template.

* Fixed customer group deletion.
    
  Now any customer associations are dropped first, to avoid database integrity
  errors.

* Stole grids and grid-based views from ``edbob``.

* Removed several references to ``edbob``.

* Replaced ``Grid.clickable`` with ``.viewable``.
    
  Clickable grid rows seemed to be more irritating than useful.  Now a view
  icon is shown instead.

* Added style for grid checkbox cells.

* Fixed FormAlchemy table rendering when underlying session is not primary.
    
  This was needed for a grid based on a LOC SMS session.

* Added grid sort arrow images.

* Improved query modification logic in alchemy grid views.

* Overhauled report views to allow easier template customization.

* Improved product UPC search so check digit is optional.

* Fixed import issue with ``views.reports`` module.


0.3a23
------

* Fixed bugs where edit links were appearing for unprivileged users.

* Added support for product codes.
    
  These are shown when viewing a product, and may be used to locate a product
  via search filters.


0.3a22
------

* Removed ``setup.cfg`` file.

* Added ``Session`` to ``rattail.pyramid`` namespace.

* Added Email Address field to Vendor CRUD views.

* Added extra key lookups for customer and product routes.
    
  Now the CRUD routes for these objects can leverage UUIDs of various related
  objects in addition to the primary object.  More should be done with this,
  but at least we have a start.

* Replaced ``forms`` module with subpackage; added some initial goodies (many
  of which are currently just imports from ``edbob``).

* Added/edited various CRUD templates for consistency.

* Modified several view modules so their Pyramid configuration is more
  "extensible."  This just means routes and views are defined as two separate
  steps, so that derived applications may inherit the route definitions if they
  so choose.

* Added Employee CRUD views; added Email Address field to index view.

* Updated ``people`` view module so it no longer derives from that of
  ``edbob``.

* Added support for, and some implementations of, extra key lookup abilities to
  CRUD views.  This allows URLs to use a "natural" key (e.g. Customer ID
  instead of UUID), for cases where that is more helpful.

* Product CRUD now uses autocomplete for Brand field.  Also, price fields no
  longer appear within an editable fieldset.

* Within Store index view, default sort is now ID instead of Name.

* Added Contact and Phone Number fields to Vendor CRUD views; added Contact and
  Email Address fields to index view.
  

0.3a21
------

- [feature] Added CRUD view and template.

- [feature] Added ``AutocompleteView``.

- [feature] Added Person autocomplete view and User CRUD views.

- [feature] Added ``id`` and ``status`` fields to Employee grid view.


0.3a20
------

- [feature] Sorted the Ordering Worksheet by product brand, description.

0.3a19
------

- [feature] Made batch creation and execution threads aware of
  `sys.excepthook`.  Updated both instances to use `rattail.threads.Thread`
  instead of `threading.Thread`.  This way if an exception occurs within the
  thread, the registered handler will be invoked.

0.3a18
------

- [bug] Label profile editing now uses stripping field renderer to avoid
  problems with leading/trailing whitespace.

- [feature] Added Inventory Worksheet report.

0.3a17
------

- [feature] Added Brand and Size fields to the Ordering Worksheet.  Also
  tweaked the template styles slightly, and added the ability to override the
  template via config.

- [feature] Added "preferred only" option to Ordering Worksheet.

0.3a16
------

- [bug] Fixed bug where requesting deletion of non-existent batch row was
  redirecting to a non-existent route.

0.3a15
------

- [bug] Fixed batch grid and CRUD views so that the execution time shows a
  pretty (and local) display instead of 24-hour UTC time.

0.3a14
------

- [feature] Added some more CRUD.  Mostly this was for departments,
  subdepartments, brands and products.  This was rather ad-hoc and still is
  probably far from complete.

- [general] Changed main batch route.

- [bug] Fixed label profile templates so they properly handle a missing or
  invalid printer spec.

0.3a13
------

- [bug] Fixed bug which prevented UPC search from working on products screen.

0.3a12
------

- [general] Fixed namespace packages, per ``setuptools`` documentation.

- [feature] Added support for ``LabelProfile.visible``.  This field may now be
  edited, and it is honored when displaying the list of available profiles to
  be used for printing from the products page.

- [bug] Fixed bug where non-numeric data entered in the UPC search field on the
  products page was raising an error.

0.3a11
------

- [bug] Fixed product label printing to handle any uncaught exception, and
  report the error message to the end user.

0.3a10
------

- [general] Updated category views and templates.  These were sorely out of
  date.

0.3a9
-----

- Add brands autocomplete view.

- Add departments autocomplete view.

- Add ID filter to vendors grid.

0.3a8
-----

- Tweak batch progress indicators.

- Add "Executed" column, filter to batch grid.

0.3a7
-----

- Add ability to restrict batch providers via config.

0.3a6
-----

- Add Vendor CRUD.

- Add Brand views.

0.3a5
-----

- Added support for GPC data type.

- Added eager import of ``rattail.sil`` in ``before_render`` hook.

- Removed ``rattail.pyramid.util`` module.

- Added initial batch support: views, templates, creation from Product grid.

- Added support for ``rattail.LabelProfile`` class.

- Improved Product grid to include filter/sort on Vendor.

- Cleaned up dependencies.

- Added ``rattail.pyramid.includeme()``.

- Added ``CustomerGroup`` CRUD view (read only).

- Added hot links to ``Customer`` CRUD view.

- Added ``Store`` index, CRUD views.

- Updated ``rattail.pyramid.views.includeme()``.

- Added ``email_preference`` to ``Customer`` CRUD.

0.3a4
-----

- Update grid and CRUD views per changes in ``edbob``.

0.3a3
-----

- Add price field renderers.

- Add/tweak lots of views for database models.

- Add label printing to product list view.

- Add (some of) ``Product`` CRUD.

0.3a2
-----

- Refactor category views.

0.3a1
-----

-  Initial port to Rattail v0.3.
