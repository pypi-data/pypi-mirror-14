<!-- DETAILED NODE INFORMATION -->
<div class="col-sm-4 col-lg-4">
    <div class="dash-unit">
        <dtitle>Node Details</dtitle>
        <hr/>
        <div class="info-user">
            <span aria-hidden="true" class="li_params fs2"></span>
        </div>
        <div class="cont" style="margin-top: 20px">
            <p><bold>{{data['chain']}}net</bold> | <ok>Network</ok></p>
            <p><bold>{{data['connections']}}</bold> | <a href="/peers">Connected Peers</a></p>
            <p><bold>{{'{:,.0f}'.format(data['blocks'])}}</bold> | <ok>Blocks</ok></p>
            % before_dec, after_dec = str(data['verificationprogress'] * 100).split('.')
            % percent = '.'.join((before_dec, after_dec[0:3]))
            <p><bold>{{percent}} %</bold> | <ok>Sync Status</ok></p>
        </div>
    </div>
</div>
