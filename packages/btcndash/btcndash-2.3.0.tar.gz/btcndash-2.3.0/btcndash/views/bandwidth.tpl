<!-- DATA TRANSFER CHART -->
% total = data['totalbytessent'] + data['totalbytesrecv']
% pcnt_in = '{:,.1f}'.format(data['totalbytesrecv'] / float(total) * 100.0)
% pcnt_out = '{:,.1f}'.format(data['totalbytessent'] / float(total) * 100.0)
<script type="text/javascript">
    $(document).ready(function() {
        info = new Highcharts.Chart({
            chart: {
                renderTo: 'load',
                margin: [0, 0, 0, 0],
                backgroundColor: null,
                plotBackgroundColor: 'none'
            },
            credits: {
                enabled: false
            },
            title: {
                text: null
            },
            tooltip: {
                formatter: function() {
                    return this.point.name +': '+ this.y +' %';
                }
            },
            series: [
                {
                borderWidth: 2,
                borderColor: '#F1F3EB',
                shadow: false,
                type: 'pie',
                name: 'Data Transfer',
                innerSize: '56%',
                data: [
                    { name: 'Incoming', y: {{pcnt_in}}, color: '#b2c831' },
                    { name: 'Outgoing', y: {{pcnt_out}}, color: '#fa1d2d' }
                ],
                dataLabels: {
                    enabled: false,
                    color: '#000000',
                    connectorColor: '#000000'
                }
            }]
        });
    });
</script>
<div class="col-sm-4 col-lg-4">
    <div class="dash-unit">
        <dtitle>Bandwidth Chart</dtitle>
        <hr/>
        <div id="load"></div>
        <h3>{{pcnt_in}}% Incoming Data</h3>
        <h3>{{pcnt_out}}% Outgoing Data</h3>
    </div>
</div>
