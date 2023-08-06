% rebase('base.tpl')
<link href="static/css/table.css" rel="stylesheet">
<style type="text/css">

    table a {
        color: black;
    }
    table tr {
        color: black;
    }
    body {
        color: white;
    }
    .dataTables_wrapper .dataTables_paginate .paginate_button {
        box-sizing: border-box;
        display: inline-block;
        min-width: 1.0em;
        padding: 0.4em 0.4em;
        margin-left: 2px;
        text-align: center;
        text-decoration: none !important;
        cursor: pointer;
        *cursor: hand;
        border: 1px solid transparent;
        border-radius: 2px;
    }
</style>
<!-- DataTables Initialization -->
<script type="text/javascript" src="static/js/jquery.dataTables.min.js"></script>
<script type="text/javascript" charset="utf-8">
    $(document).ready(function() {
        $('#dt1').dataTable();
    } );
</script>
<div class="container">
    <!-- FIRST ROW OF BLOCKS -->
    <div class="row">
        <!-- PEER INFORMATION -->
        <div class="col-sm-12 col-lg-12">
            <table class="display" id="dt1">
                <thead>
                    <tr>
                        <th>IP and Port</th>
                        <th>Client</th>
                        <th>Version</th>
                        <th>Service Bit</th>
                        <th>Ping Time (Sec)</th>
                    </tr>
                </thead>
                <tbody>
                    % for peer in data['peerinfo']:
                    <tr class="even gradeU">
                        <td class="center"><a href="{{data['ip_info_url'] + peer['addr'].partition(':')[0]}}">{{peer['addr']}}</a></td>
                        <td class="center">{{peer['subver']}}</td>
                        <td class="center">{{peer['version']}}</td>
                        <td class="center">{{int(peer['services'])}}</td>
                        <td class="center">{{'{:,.4f}'.format(peer['pingtime'])}}</td>
                    </tr>
                    % end
                </tbody>
            </table>
        </div>
    </div><!-- /row -->
</div><!-- /container -->
