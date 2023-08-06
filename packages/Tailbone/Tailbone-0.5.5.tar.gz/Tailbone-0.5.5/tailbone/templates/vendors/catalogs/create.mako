## -*- coding: utf-8 -*-
<%inherit file="/newbatch/create.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  <script type="text/javascript">

    var vendormap = {
        % for i, parser in enumerate(parsers, 1):
            '${parser.key}': ${parser.vendormap_value|n}${',' if i < len(parsers) else ''}
        % endfor
    };

    $(function() {

        if ($('#VendorCatalog--parser_key option:first').is(':selected')) {
            $('#VendorCatalog--vendor_uuid-container').hide();
        } else {
            $('#VendorCatalog--vendor_uuid').val('');
            $('#VendorCatalog--vendor_uuid-display').hide();
            $('#VendorCatalog--vendor_uuid-display button').show();
            $('#VendorCatalog--vendor_uuid-textbox').val('');
            $('#VendorCatalog--vendor_uuid-textbox').show();
            $('#VendorCatalog--vendor_uuid-container').show();
        }

        $('#VendorCatalog--parser_key').change(function() {
            if ($(this).find('option:first').is(':selected')) {
                $('#VendorCatalog--vendor_uuid-container').hide();
            } else {
                var vendor = vendormap[$(this).val()];
                if (vendor) {
                    $('#VendorCatalog--vendor_uuid').val(vendor.uuid);
                    $('#VendorCatalog--vendor_uuid-textbox').hide();
                    $('#VendorCatalog--vendor_uuid-display span:first').text(vendor.name);
                    $('#VendorCatalog--vendor_uuid-display button').hide();
                    $('#VendorCatalog--vendor_uuid-display').show();
                    $('#VendorCatalog--vendor_uuid-container').show();
                } else {
                    $('#VendorCatalog--vendor_uuid').val('');
                    $('#VendorCatalog--vendor_uuid-display').hide();
                    $('#VendorCatalog--vendor_uuid-display button').show();
                    $('#VendorCatalog--vendor_uuid-textbox').val('');
                    $('#VendorCatalog--vendor_uuid-textbox').show();
                    $('#VendorCatalog--vendor_uuid-container').show();
                    $('#VendorCatalog--vendor_uuid-textbox').focus();
                }
            }
        });

    });
  </script>
</%def>

${parent.body()}
