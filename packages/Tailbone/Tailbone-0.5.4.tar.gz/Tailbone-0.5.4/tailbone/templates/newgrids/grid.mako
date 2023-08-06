## -*- coding: utf-8 -*-
<div ${format_attrs(**grid.get_div_attrs())}>
  <table>
    <thead>
      <tr>
        % if grid.checkboxes:
            <th class="checkbox">${h.checkbox('check-all')}</th>
        % endif
        % for column in grid.iter_visible_columns():
            ${grid.column_header(column)}
        % endfor
        % if grid.show_actions_column:
            <th class="actions">Actions</th>
        % endif
      </tr>
    </thead>
    <tbody>
      % for i, row in enumerate(grid.iter_rows(), 1):
          <tr ${format_attrs(**grid.get_row_attrs(row, i))}>
            % if grid.checkboxes:
                <td class="checkbox">${grid.render_checkbox(row)}</td>
            % endif
            % for column in grid.iter_visible_columns():
                <td ${format_attrs(**grid.get_cell_attrs(row, column))}>${grid.render_cell(row, column)}</td>
            % endfor
            % if grid.show_actions_column:
                <td class="actions">
                  ${grid.render_actions(row)}
                </td>
            % endif
          </tr>
      % endfor
    </tbody>
  </table>
  % if grid.pageable and grid.pager:
      <div class="pager">
        <p class="showing">
          showing ${grid.pager.first_item} thru ${grid.pager.last_item} of ${grid.pager.item_count}
          % if grid.pager.page_count > 1:
              (page ${grid.pager.page} of ${grid.pager.page_count})
          % endif
        </p>
        <p class="page-links">
          ${h.select('pagesize', grid.pager.items_per_page, grid.get_pagesize_options())}
          per page&nbsp;
          ${grid.pager.pager('$link_first $link_previous ~1~ $link_next $link_last', symbol_next='next', symbol_previous='prev', partial=1)}
        </p>
      </div>
  % endif
</div>
