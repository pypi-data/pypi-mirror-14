<!-- DONATE ADDRESS -->
<div class="col-sm-4 col-lg-4">
    <div class="dash-unit">
        <dtitle>Donate Address</dtitle>
        <hr/>
        <div class="cont">
            % donate = data['donate_url'] + data['donate_address']
            % qr_url = data['qr_url'] + data['qr_param'] + data['donate_address']
            <p><a href='{{donate}}'><img src='{{qr_url}}' alt='QRCode' /></a></p>
        </div>
    </div>
</div>
