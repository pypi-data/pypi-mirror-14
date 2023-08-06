<!-- GENERAL NODE INFORMATION -->
<div class="col-sm-4 col-lg-4">
    <div class="dash-unit">
        <dtitle>Bitcoin Node Information</dtitle>
        <hr/>
        <div class="info-user">
            <span aria-hidden="true" class="li_display fs2"></span>
        </div>
        <br/>
        % map_url = data['map_url'].format(data['lat'], data['lon'])
        % ip = ':'.join([data['server_ip_public'], str(data['node_port'])])
        <h1>{{data['node_name']}}</h1>
        <h1>{{ip}}</h1>
        <h3><a href='{{map_url}}'>{{data['server_location']}}</a></h3>
        <div class="cont">
            % import time
            % update_time = time.strftime("%Y-%m-%d %H:%M:%S")
            <p>Stats Last Updated:<br/>{{update_time}}</p>
        </div>
    </div>
</div>
