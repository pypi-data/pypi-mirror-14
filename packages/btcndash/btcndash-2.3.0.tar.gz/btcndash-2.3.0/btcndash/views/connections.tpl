<div class="col-sm-4 col-lg-4">
    <!-- CONNECTIONS -->
    <div class="half-unit">
        <dtitle>Connections</dtitle>
        <hr/>
        <div class="cont">
            <h2>{{data['connections']}}</h2>
            <h3><a href="/peers">Connected Peers</a></h3>
        </div>
    </div>
    <!-- TRANSACTIONS -->
    <div class="half-unit">
        <dtitle>Transactions</dtitle>
        <hr/>
        <div class="cont">
            % tx_count = '{:,}'.format(len(data['rawmempool']))
            <h2>{{tx_count}}</h2>
            <h3><a href="/tx">Recent Transactions</a></h3>
        </div>
    </div>
</div>
