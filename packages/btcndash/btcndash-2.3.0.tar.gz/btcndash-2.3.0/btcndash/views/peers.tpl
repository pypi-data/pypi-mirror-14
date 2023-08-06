% rebase('base.tpl')
<style type="text/css">
    .dash-unit {
        height:100%;
    }
</style>
<div class="container">
        <!-- FIRST ROW OF BLOCKS -->
        <div class="row">
        <!-- PEER INFORMATION -->
        <div class="col-sm-12 col-lg-12">
             <div class="dash-unit">
                  <dtitle>Connected Peers</dtitle>
                  <hr/>
                  <div class="info-user">
                      <span aria-hidden="true" class="li_world fs2"></span>
                  </div>
                  <br/>
                  <h1>Connected Peers</h1>
                  <div class="cont">
                      <p>
                          % for peer in data['peerinfo']:
                              <a href="{{data['ip_info_url'] + peer['addr'].partition(':')[0]}}">{{peer['addr']}}</a> ({{peer['subver']}})<br/>
                          % end
                      </p>
                  </div>
             </div>
         </div>
      </div><!-- /row -->
</div><!-- /container -->
