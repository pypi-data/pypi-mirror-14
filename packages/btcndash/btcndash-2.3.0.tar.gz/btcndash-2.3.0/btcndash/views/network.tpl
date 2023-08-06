<!-- NETWORK STATS -->
<div class="col-sm-4 col-lg-4">
    <div class="dash-unit">
        <dtitle>Network Information</dtitle>
        <hr/>
        <div class="cont">
            % diff = '{:,.2f}'.format(data['difficulty'])
            % block_height = '{:,}'.format(data['blocks'])
            % hashrate = '{:,.1f}'.format(float(data['networkhashps']) / 1.0E12)
            % block_url = data['block_height_url'] + str(data['blocks'])
            <h2>{{block_height}}</a></h2>
            <h3><a href="{{block_url}}">Block Height</a></h3>
            <h2>{{hashrate}} Th/s</h2>
            <h3><a href='{{data['hash_diff_url']}}'>Hash Rate</a></h3>
            <h2>{{diff}}</a></h2>
            <h3><a href='{{data['hash_diff_url']}}'>Difficulty</a></h3>
        </div>
    </div>
</div>
