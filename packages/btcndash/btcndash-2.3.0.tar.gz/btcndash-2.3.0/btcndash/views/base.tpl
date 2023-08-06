<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    
    <title>{{data['title'] or 'Bitcoin Node Status'}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <link href="static/css/bootstrap.css" rel="stylesheet" />
    <link href="static/css/main.css" rel="stylesheet" />
    <link href="static/css/font-style.css" rel="stylesheet" />
    <script type="text/javascript" src="static/js/jquery-1.12.2.min.js"></script>

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <link rel="shortcut icon" href="static/img/favicon.ico" type="image/icon" />

    <!-- Google Fonts call. Font Used Open Sans & Raleway -->
    <link href="http://fonts.googleapis.com/css?family=Raleway:400,300" rel="stylesheet" type="text/css" />
    <link href="http://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css" />
    
</head>
<body>
    <!-- NAVIGATION MENU -->
    <div class="navbar-nav navbar-inverse navbar-fixed-top">
        <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="/"><img src="static/img/bitcoin_logo_qt.png" width="18" height="18" alt=""/>{{data['header_title']}}</a>
        </div> 
        </div>
    </div>
    {{!base}}
    <div id="footerwrap">
        <footer class="clearfix"></footer>
        <div class="container">
            <div class="row">
                <div class="col-sm-12 col-lg-12">
                    <p>
                        <a href="https://bitbucket.org/mattdoiron/btcndash">BTCnDash</a>
                        : Bitcoin Node Dashboard - Copyright 2014-2016<br/>
                        Donate to: <a href='{{data['donate_url']}}'>{{data['donate_address']}}</a>
                    </p>
                    % import time
                    % update_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    <p>Stats Last Updated: {{update_time}}</p>
                </div>
            </div><!-- /row -->
        </div><!-- /container -->
    </div><!-- /footerwrap -->

    <!-- javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script type="text/javascript" src="static/js/bootstrap.js"></script>
    <script type="text/javascript" src="static/js/highcharts-4.2.3.min.js"></script>

</body></html>
