## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">Create Products Batch</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Back to Products", url('products'))}</li>
</%def>

<div class="form">

  ${h.form(request.current_route_url())}

  <div class="field-wrapper">
    <label for="provider">Batch Type</label>
    <div class="field">
      ${h.select('provider', None, providers)}
    </div>
  </div>

  <div class="buttons">
    ${h.submit('create', "Create Batch")}
    ${h.link_to("Cancel", url('products'), class_='button')}
  </div>

  ${h.end_form()}

</div>
