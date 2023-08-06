## -*- coding: utf-8 -*-
<%inherit file="/master/index.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  <style type="text/css">

    table.label-printing th {
        font-weight: normal;
        padding: 0px 0px 2px 4px;
        text-align: left;
    }

    table.label-printing td {
        padding: 0px 0px 0px 4px;
    }

    table.label-printing #label-quantity {
        text-align: right;
        width: 30px;
    }

    div.grid table tbody td.size,
    div.grid table tbody td.regular_price_uuid,
    div.grid table tbody td.current_price_uuid {
        padding-right: 6px;
        text-align: right;
    }
    
    div.grid table tbody td.labels {
        text-align: center;
    }
    
  </style>
  % if label_profiles and request.has_perm('products.print_labels'):
      <script type="text/javascript">

      $(function() {
          $('.newgrid-wrapper').on('click', 'a.print_label', function() {
              var quantity = $('table.label-printing #label-quantity');
              if (isNaN(quantity.val())) {
                  alert("You must provide a valid label quantity.");
                  quantity.select();
                  quantity.focus();
              } else {
                  quantity = quantity.val();
                  var data = {
                      product: get_uuid(this),
                      profile: $('#label-profile').val(),
                      quantity: quantity
                  };
                  console.log(data);
                  $.get('${url('products.print_labels')}', data, function(data) {
                      if (data.error) {
                          alert("An error occurred while attempting to print:\n\n" + data.error);
                      } else if (quantity == '1') {
                          alert("1 label has been printed.");
                      } else {
                          alert(quantity + " labels have been printed.");
                      }
                  });
              }
              return false;
          });
      });

      </script>
  % endif
</%def>

<%def name="grid_tools()">
  % if label_profiles and request.has_perm('products.print_labels'):
      <table class="label-printing">
        <thead>
          <tr>
            <th>Label</th>
            <th>Qty.</th>
          </tr>
        </thead>
        <tbody>
          <td>
            <select name="label-profile" id="label-profile">
              % for profile in label_profiles:
                  <option value="${profile.uuid}">${profile.description}</option>
              % endfor
            </select>
          </td>
          <td>
            <input type="text" name="label-quantity" id="label-quantity" value="1" />
          </td>
        </tbody>
      </table>
  % endif
</%def>

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('batches.create'):
      <li>${h.link_to("Create Batch from Results", url('products.create_batch'))}</li>
  % endif
</%def>

${parent.body()}
