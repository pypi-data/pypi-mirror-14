## -*- coding: utf-8 -*-
${h.text(name, value=value)}
<script type="text/javascript">
  $(function() {
      $('input[name="${name}"]').datepicker({
          changeYear: ${'true' if change_year else 'false'},
          dateFormat: 'yy-mm-dd'
      });
  });
</script>
