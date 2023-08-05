<!-- MEMPOOL SUMMARY -->
<div class="col-sm-4 col-lg-4">
    <div class="dash-unit">
        <dtitle>Mempool Information</dtitle>
        <hr/>
        <div class="cont">
            <h2 style="margin-top: -20px;">{{'{:,.0f}'.format(data['size'])}}</h2>
            <h3><a href="/tx">Transaction Count</a></h3>
            <h2>{{'{:,.1f}'.format(data['bytes'] / 1048576)}} MB</h2>
            <h3>Total Size of All Transactions</h3>
            <h2>{{'{:,.1f}/{:,.1f}'.format(data['usage'] / 1048576.0, data['maxmempool'] / 1048576.0)}} MB</h2>
            <div class="progress">
                % percent = float(data['usage']) / float(data['maxmempool']) * 100.0
                <div class="progress-bar" role="progressbar" aria-valuenow="{{percent}}" aria-valuemin="0" aria-valuemax="100" style="width:{{percent}}%;">
                    <span class="sr-only">{{percent}}% Complete</span>
                </div>
            </div>
            <h3>Memory Use</h3>
        </div>
    </div>
</div>
