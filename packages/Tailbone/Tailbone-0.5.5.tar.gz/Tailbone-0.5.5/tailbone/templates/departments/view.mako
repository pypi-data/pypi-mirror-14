## -*- coding: utf-8 -*-
<%inherit file="/master/view.mako" />

${parent.body()}

<h2>Employees</h2>

% if employees:
    <p>The following employees are assigned to this department:</p>
    ${employees.render_grid()|n}
% else:
    <p>No employees are assigned to this department.</p>
% endif
