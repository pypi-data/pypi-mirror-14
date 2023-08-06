<!-- BITNODES INFORMATION -->
<div class="col-sm-4 col-lg-4">
    <div class="dash-unit">
        <dtitle>Bitnodes Status</dtitle>
        <hr/>
        <div class="info-user">
            <span aria-hidden="true" class="li_star fs2"></span>
        </div>
        <div class="cont" style="margin-top: 20px">
            % bitnodes_status = data['bitnodes']['status']['status']
            % bitnodes_rank = data['bitnodes']['rank']['rank']
            % bitnodes_pix = data['bitnodes']['rank']['peer_index']
            % bitnodes_verified = data['bitnodes']['status']['verified']
            % bitnodes_asn = data['bitnodes']['status']['data'][-2]
            % bitnodes_upsince = data['bitnodes']['status']['data'][2]
            % import datetime as dt
            % upsince = dt.datetime.fromtimestamp(bitnodes_upsince).strftime('%c')
            <p>
                <bold>{{bitnodes_pix}}</bold> | <ok>PIX</ok>&nbsp;&nbsp;&nbsp;&nbsp;
                <bold>{{bitnodes_rank}}</bold> | <ok>Rank</ok>
            </p>
            <p>
                <bold>{{str(bitnodes_verified)}}</bold> | <ok>Verified</ok>&nbsp;&nbsp;&nbsp;&nbsp;
                <bold>{{bitnodes_status}}</bold> | <a href="{{data['bitnodes']['bitnodes_link']}}">Status</a>
            </p>
            <p><bold>{{bitnodes_asn}}</bold> | <ok>ASN</ok></p>
            <p>{{upsince}} | <ok>Up Since</ok></p>
        </div>
    </div>
</div>
