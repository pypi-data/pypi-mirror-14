<!-- DATA TRANSFER SUMMARY -->
<div class="col-sm-4 col-lg-4">
    <div class="dash-unit">
        <dtitle>Bandwidth Summary</dtitle>
        <hr/>
        <div class="cont">
            % sent = '{:,.1f}'.format(data['totalbytessent'] / 1048576.0)
            % recv = '{:,.1f}'.format(data['totalbytesrecv'] / 1048576.0)
            % total = '{:,.3f}'.format((data['totalbytessent'] + data['totalbytesrecv']) / 1073741824.0)
            <h2>{{sent}} MB</h2>
            <h3>Sent</h3>
            <h2>{{recv}} MB</h2>
            <h3>Received</h3>
            <h2>{{total}} GB</h2>
            <h3>Total</h3>
        </div>
    </div>
</div>
