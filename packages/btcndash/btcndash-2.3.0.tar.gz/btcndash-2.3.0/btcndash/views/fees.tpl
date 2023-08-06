<!-- FEE SUMMARY -->
<div class="col-sm-4 col-lg-4">
    <div class="dash-unit">
        <dtitle>Network Fee Summary</dtitle>
        <hr/>
        <div class="info-user">
            <span aria-hidden="true" class="li_banknote fs2"></span>
        </div>
        <div class="cont">
            % fastestfee = data['21co_fees']['fastestFee']
            % half_hour_fee = data['21co_fees']['halfHourFee']
            % hour_fee = data['21co_fees']['hourFee']
            % fee_summary_url = data['fee_url'].replace('api/v1/fees/', '')
            <p><bold>{{fastestfee}} </bold> Satoshi/Byte | <ok>Fastest</ok></p>
            <p><bold>{{half_hour_fee}} </bold> Satoshi/Byte | <ok>Half-hour</ok></p>
            <p><bold>{{hour_fee}} </bold> Satoshi/Byte | <ok>Hour</ok></p>
            <p><a href="{{fee_summary_url}}"><ok>Detailed Breakdown</ok></a></p>
        </div>
    </div>
</div>
