<html>
  <body>
    <h3>Warnings for ${host_title} -> ${local_title} data import</h3>
    % if dry_run:
        <p>
          <em><strong>NOTE:</strong>&nbsp; This was a dry run only; no data was harmed
          in the making of this email.</em>
        </p>
    % endif
    <p>
      Generally the periodic data import is expected to be a precaution only,
      in order to detect and fix local data which has fallen out of sync from the
      data authority, e.g. your POS.&nbsp; It is normally intended that proper
      real-time operation (e.g. a 'datasync' daemon) <em>should</em> be enough to
      keep things in sync; therefore any net changes which occur as a result of this
      periodic import process are considered "warnings".
    </p>
      The following is a list of changes which occurred during the latest import run.&nbsp;
      % if not dry_run:
          (Note that this was not a dry run; these changes have been committed
          to the ${local_title} system.)&nbsp;
      % endif
      Please investigate at your convenience.
    </p>
    <ul>
      % for model, (created, updated, deleted) in updates.iteritems():
          <li>
            <a href="#${model}">${model}</a>
            - ${len(created)} created, ${len(updated)} updated, ${len(deleted)} deleted
          </li>
      % endfor
    </ul>
    <p>
      Full command was:&nbsp; <code>${argv}</code>
    <p>
    % for model, (created, updated, deleted) in updates.iteritems():
        <h4><a name="${model}">${model}</a></h4>
        % for label, records in (('created', created), ('updated', updated), ('deleted', deleted)):
            % if records:
                % if len(records) == 1:
                    <p>1 record was <strong>${label}:</strong></p>
                % else:
                    <p>${len(records)} records were <strong>${label}:</strong></p>
                % endif
                <ul>
                  % for record in records:
                      <li>${render_record(record)}</li>
                  % endfor
                </ul>
            % endif
        % endfor
    % endfor
  </body>
</html>
