## -*- coding: utf-8 -*-
<%inherit file="/master/view.mako" />

${parent.body()}

<h2>People</h2>
% if instance.people:
    <p>Customer account is associated with the following people:</p>
    <div class="grid clickable">
      <table>
        <thead>
          <th>First Name</th>
          <th>Last Name</th>
        </thead>
        <tbody>
          % for i, person in enumerate(instance.people, 1):
              <tr class="${'odd' if i % 2 else 'even'}" url="${url('people.view', uuid=person.uuid)}">
                <td>${person.first_name or ''}</td>
                <td>${person.last_name or ''}</td>
              </tr>
          % endfor
        </tbody>
      </table>
    </div>
% else:
    <p>Customer account is not associated with any people.</p>
% endif

<h2>Groups</h2>
% if instance.groups:
    <p>Customer account belongs to the following groups:</p>
    <div class="grid clickable">
      <table>
        <thead>
          <th>ID</th>
          <th>Name</th>
        </thead>
        <tbody>
          % for i, group in enumerate(instance.groups, 1):
              <tr class="${'odd' if i % 2 else 'even'}" url="${url('customergroups.view', uuid=group.uuid)}">
                <td>${group.id}</td>
                <td>${group.name or ''}</td>
              </tr>
          % endfor
        </tbody>
      </table>
    </div>
% else:
    <p>Customer account doesn't belong to any groups.</p>
% endif
