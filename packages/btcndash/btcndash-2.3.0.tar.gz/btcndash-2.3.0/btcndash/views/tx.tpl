% rebase('base.tpl')
<style type="text/css">
.dash-unit {		
    height:100%;
}
</style>
<div class="container">
    <!-- FIRST ROW OF BLOCKS -->
    <div class="row">
        <!-- NODE INFORMATION -->
        <div class="col-sm-12 col-lg-12">
            <div class="dash-unit">
                <dtitle>Transactions</dtitle>
                <hr/>
                <div class="info-user">
                    <span aria-hidden="true" class="li_banknote fs2"></span>
                </div>
                <br/>
                <h1>Last 25 Transactions</h1>
                <div class="cont">
                    <p>
                        % for tx in data['rawmempool'][-25:]:
                            <a href="{{data['tx_info_url'] + tx}}">{{tx}}</a><br/>
                        % end
                    </p>
                </div>
            </div>
        </div>
    </div><!-- /row -->
</div><!-- /container -->
