## -*- coding: utf-8 -*-
<!DOCTYPE html>
<html style="direction: ltr;" xmlns="http://www.w3.org/1999/xhtml" lang="en-us">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>${self.global_title()} &raquo; ${capture(self.title)}</title>
    <link rel="icon" type="image/x-icon" href="${request.static_url('tailbone:static/img/rattail.ico')}" />
    ${self.core_javascript()}
    ${self.core_styles()}
    ${self.head_tags()}
  </head>

  <body>

    <div id="body-wrapper">

      <div id="header">
        <h1>${h.link_to(capture(self.global_title), url('home'))}</h1>
        <h1 class="title">&raquo; ${self.title()}</h1>
        <div class="login">
          % if request.user:
              ${h.link_to(request.user.display_name, url('change_password'))}
              (${h.link_to("logout", url('logout'))})
          % else:
              ${h.link_to("login", url('login'))}
          % endif
        </div>
      </div><!-- header -->

      <ul class="menubar">
        <li>
          <a>Products</a>
          <ul>
            <li>${h.link_to("Products", url('products'))}</li>
            <li>${h.link_to("Brands", url('brands'))}</li>
          </ul>
        </li>
        <li>
          <a>Customers</a>
          <ul>
            <li>${h.link_to("Customers", url('customers'))}</li>
            <li>${h.link_to("Customer Groups", url('customer_groups'))}</li>
          </ul>
        </li>
        <li>
          <a>Employees</a>
          <ul>
            <li>${h.link_to("Employees", url('employees'))}</li>
          </ul>
        </li>
        <li>
          <a>Vendors</a>
          <ul>
            <li>${h.link_to("Vendors", url('vendors'))}</li>
          </ul>
        </li>
        % if request.has_perm('batches.list'):
            <li>
              <a>Batches</a>
              <ul>
                <li>${h.link_to("Batches", url('batches'))}</li>
              </ul>
            </li>
        % endif
        <li>
          <a>Stores</a>
          <ul>
            <li>${h.link_to("Stores", url('stores'))}</li>
            <li>${h.link_to("Departments", url('departments'))}</li>
            <li>${h.link_to("Subdepartments", url('subdepartments'))}</li>
          </ul>
        </li>
        % if request.has_perm('users.list') or request.has_perm('roles.list'):
            <li>
              <a>Auth</a>
              <ul>
                % if request.has_perm('users.list'):
                    <li>${h.link_to("Users", url('users'))}</li>
                % endif
                % if request.has_perm('roles.list'):
                    <li>${h.link_to("Roles", url('roles'))}</li>
                % endif
              </ul>
            </li>
        % endif
      </ul>

      <div id="body">

        % if request.session.peek_flash('error'):
            <div class="error-messages">
              % for error in request.session.pop_flash('error'):
                  <div class="ui-state-error ui-corner-all">
                    <span style="float: left; margin-right: .3em;" class="ui-icon ui-icon-alert"></span>
                    ${error}
                  </div>
              % endfor
            </div>
        % endif

        % if request.session.peek_flash():
            <div class="flash-messages">
              % for msg in request.session.pop_flash():
                  <div class="ui-state-highlight ui-corner-all">
                    <span style="float: left; margin-right: .3em;" class="ui-icon ui-icon-info"></span>
                    ${msg|n}
                  </div>
              % endfor
            </div>
        % endif

        ${self.body()}

      </div><!-- body -->

    </div><!-- body-wrapper -->

    <div id="footer">
      powered by ${h.link_to("Rattail", 'http://rattailproject.org/', target='_blank')}
    </div>

  </body>
</html>

<%def name="global_title()">Tailbone</%def>

<%def name="title()"></%def>

<%def name="core_javascript()">
  ${h.javascript_link('https://code.jquery.com/jquery-1.11.3.min.js')}
  ${h.javascript_link('https://code.jquery.com/ui/1.11.4/jquery-ui.min.js')}
  ${h.javascript_link(request.static_url('tailbone:static/js/lib/jquery.ui.menubar.js'))}
  ${h.javascript_link(request.static_url('tailbone:static/js/lib/jquery.loadmask.min.js'))}
  ${h.javascript_link(request.static_url('tailbone:static/js/lib/jquery.ui.timepicker.js'))}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.js'))}
</%def>

<%def name="core_styles()">
  ${h.stylesheet_link(request.static_url('tailbone:static/css/normalize.css'))}
  ${self.jquery_theme()}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/jquery.ui.menubar.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/jquery.loadmask.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/jquery.ui.timepicker.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/jquery.ui.tailbone.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/base.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/layout.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/grids.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/filters.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/forms.css'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/newgrids.css'))}
</%def>

<%def name="jquery_theme()">
  ${h.stylesheet_link('https://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.min.css')}
</%def>

<%def name="head_tags()"></%def>
