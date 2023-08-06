## -*- coding: utf-8 -*-
<div class="newfilters">

  ${form.begin(method='get')}
    <input type="hidden" name="reset-to-default-filters" value="false" />
    <input type="hidden" name="save-current-filters-as-defaults" value="false" />

    <fieldset>
      <legend>Filters</legend>
      % for filtr in form.iter_filters():
          <div class="filter" id="filter-${filtr.key}" data-key="${filtr.key}"${' style="display: none;"' if not filtr.active else ''|n}>
            ${form.checkbox('{0}-active'.format(filtr.key), class_='active', id='filter-active-{0}'.format(filtr.key), checked=filtr.active)}
            <label for="filter-active-${filtr.key}">${filtr.label}</label>
            <div class="inputs">
              ${form.filter_verb(filtr)}
              ${form.filter_value(filtr)}
            </div>
          </div>
      % endfor
    </fieldset>

    <div class="buttons">
      ${form.tag('button', type='submit', id='apply-filters', c="Apply Filters")}
      <select id="add-filter">
        <option value="">Add a Filter</option>
        % for filtr in form.iter_filters():
            <option value="${filtr.key}"${' disabled="disabled"' if filtr.active else ''|n}>${filtr.label}</option>
        % endfor
      </select>
      ${form.tag('button', type='button', id='default-filters', c="Default View")}
      ${form.tag('button', type='button', id='clear-filters', c="No Filters")}
      % if allow_save_defaults and request.user:
          ${form.tag('button', type='button', id='save-defaults', c="Save Defaults")}
      % endif
    </div>

  ${form.end()}
</div><!-- newfilters -->
