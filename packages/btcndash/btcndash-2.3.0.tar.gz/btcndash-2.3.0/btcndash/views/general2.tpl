<!-- NODE INFORMATION -->
<div class="col-sm-4 col-lg-4">
    <div class="dash-unit">
        <dtitle>Node Information</dtitle>
        <hr/>
        <div class="info-user">
            <span aria-hidden="true" class="li_display fs2"></span>
        </div>
        % map_url = data['map_url'].format(data['lat'], data['lon'])
        % ip = ':'.join([data['server_ip_public'], str(data['node_port'])])
        <h2>{{data['node_name']}}</h2>
        <h1>{{data['subversion']}} ({{data['protocolversion']}})</h1>
        <h1>{{ip}}</h1>
        <h3><a href='{{map_url}}'>{{data['server_location']}}</a></h3>
        <div class="cont">
            <p>Services:<br/>{{data['services_offered']}}</p>
        </div>
    </div>
</div>
