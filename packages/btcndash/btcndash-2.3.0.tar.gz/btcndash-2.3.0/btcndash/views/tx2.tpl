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
        <!-- TRANSACTION INFORMATION -->
        <div class="col-sm-12 col-lg-12">
            <table class="display" id="dt1">
                <thead>
                    <tr>
                        <th>Transaction ID</th>
                        <th>Received Time (Server Local)</th>
                        <th>Size (kB)</th>
                        <th>Fee (BTC)</th>
                    </tr>
                </thead>
                <tbody>
                    % import datetime as dt
                    % for txid in list(data['rawmempool'].keys())[:data['tx_summary_limit']]:
                    % tx = data['rawmempool'][txid]
                    <tr class="even gradeU">
                        <td class="center"><a href="{{data['tx_info_url'] + txid}}">{{txid}}</a></td>
                        <td class="center">{{dt.datetime.fromtimestamp(tx['time']).strftime('%c')}}</td>
                        <td class="center">{{'{:,.3f}'.format(tx['size'] / 1024.0)}}</td>
                        <td class="center">{{'{:,.8f}'.format(tx['fee'])}}</td>
                    </tr>
                    % end
                </tbody>
            </table>
        </div>
    </div><!-- /row -->
</div><!-- /container -->
