<!-- NODE INFORMATION -->
<div class="col-sm-4 col-lg-4">
    <div class="dash-unit">
        <dtitle>Node Information</dtitle>
        <hr/>
        <div class="info-user">
            <span aria-hidden="true" class="li_display fs2"></span>
        </div>
        <h2>Bitcoin Node</h2>
        <h1>{{data['subversion']}} ({{data['protocolversion']}})</h1>
        <h1>{{data['ip']}}</h1>
        <h3><a href='{{data['map_url']}}'>{{data['loc']}}</a></h3>
        <div class="cont">
            <p>Services:<br/>{{data['services_offered']}}</p>
        </div>
    </div>
</div>
