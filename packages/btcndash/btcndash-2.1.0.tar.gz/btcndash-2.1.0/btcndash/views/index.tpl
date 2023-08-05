% rebase('base.tpl')
<div class="container">
    % for row in page_info['tiles']:
        <!-- Start of row -->
        <div class="row">
            % for tile_name in row:
                % include(tiles[tile_name]['template'], data=data)
            % end
        </div> <!-- /row -->
    % end
</div> <!-- /container -->
