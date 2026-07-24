let page_style = 'black';

function theme(){
    return page_style;
}

function ChangeTheme(username){
    page_style = courent_theme;

    let main = document.getElementById('courent_theme');
    let input = document.getElementById('theme_input');
    let img = document.getElementById('img');
    let main_items_background = document.getElementsByClassName('main_items_background');
    let text_fix = document.getElementsByClassName('text_fix');

    let login_pic = null;
    if(document.getElementById('login_pic')){
       login_pic = document.getElementById('login_pic');;
    }

    let find_by_name = null;
    if(document.querySelector('.find_by_name')){
       find_by_name = document.querySelector('.find_by_name');
    }

    let find_by_name2 = null;
    if(document.querySelector('.find_by_name2')){
       find_by_name2 = document.querySelector('.find_by_name2');
    }

    let find_by_name2_container = null;
    if(document.querySelector('.find_by_name2_container')){
       find_by_name2_container = document.querySelector('.find_by_name2_container');
    }
    
    let catalog = null;
    if(document.querySelector('.catalog')){
       catalog = document.querySelector('.catalog');
    }

    let new_products_h4 = null;
    if(document.querySelectorAll('.new_products_h4')){
       new_products_h4 = document.querySelectorAll('.new_products_h4');
    }

    let filter = null;
    if (document.querySelector('.filter')){
        filter = document.querySelector('.filter');
    }

    let btn_logo = document.querySelectorAll('.btn_logo');
    if (username){
        let nickname = document.getElementById('nickname');
    }

    let fonts = null;
    if (document.querySelectorAll('.font')){
        fonts = document.querySelectorAll('.font');
    }

    let auth_form_input = null;
    if (document.querySelectorAll('.auth_form_input')){
        auth_form_input = document.querySelectorAll('.auth_form_input');
    }

    let auth_button = null;
    if (document.querySelectorAll('.auth_button')){
        auth_button = document.querySelectorAll('.auth_button');
    }
    let body = document.getElementById('products-list-container');
    let font1 = document.getElementsByClassName('card_info_list_font');
    let font2 = document.getElementsByClassName('gray_font');

    let textC_gr = document.querySelectorAll('.text-content');

    let filterList_tags = document.querySelectorAll('.checkbox-item');
    let filterList_tags_checkBoxes = document.querySelectorAll('input');

    let filter_blocks_grid = null;
    if (document.querySelectorAll('.filter_blocks_grid')){
        filter_blocks_grid = document.querySelectorAll('.filter_blocks_grid');
    }

    let choices__list = null;
    if (document.querySelectorAll('.choices__list--dropdown')){
        choices__list = document.querySelectorAll('.choices__list--dropdown');
    }

    let basket = null;
    if (document.querySelectorAll('.basket')){
        basket = document.querySelectorAll('.basket');
    }

    let choices__list__single = null;
    if (document.querySelectorAll('.choices__list--single').length !== 0){
        choices__list__single = document.querySelectorAll('.choices__list--single');
    } else {
        if (courent_theme == 'black') {
            document.documentElement.style.setProperty('--choices__list__single__background__fix', 'rgb(30, 30, 30)');
            document.documentElement.style.setProperty('--choices__list__single__color__fix', 'rgb(230, 230, 230)');
        } else {
            document.documentElement.style.setProperty('--choices__list__single__background__fix', 'rgb(255, 255, 255)');
            document.documentElement.style.setProperty('--choices__list__single__color__fix', 'rgb(30, 30, 30)');
        }
    }

    let select_sort = null;
    if (document.querySelectorAll('.choices__list')){
        select_sort = document.querySelectorAll('.choices__list');
    }

    let dropdown_content = null;
    if (document.querySelectorAll('.dropdown-content')){
        dropdown_content = document.querySelectorAll('.dropdown-content');
    }

    let dropdown_content_linear_gr = null;
    if (document.querySelectorAll('.dropdown-content-linear-gr')){
        dropdown_content_linear_gr = document.querySelectorAll('.dropdown-content-linear-gr');
    }

    let you_container_dop_block_text = null;
    if (document.querySelectorAll('.you_container_dop_block_text')){
        you_container_dop_block_text = document.querySelectorAll('.you_container_dop_block_text');
    }

    let comments_container = null;
    if (document.querySelectorAll('.comments_container')){
        comments_container = document.querySelectorAll('.comments_container');
    }

    let main_characters_img_block_fade = null;
    if (document.querySelectorAll('.main_characters_img_block_fade')){
        main_characters_img_block_fade = document.querySelectorAll('.main_characters_img_block_fade');
    }

    let related_product_link = null;
    if (document.querySelectorAll('.related_product_link')){
        related_product_link = document.querySelectorAll('.related_product_link');
    }

    let all_comments_container = null;
    if (document.querySelectorAll('.all_comments_container')){
        all_comments_container = document.querySelectorAll('.all_comments_container');
    }

    let answer = null;
    if (document.querySelectorAll('.answer')){
        answer = document.querySelectorAll('.answer');
    }

    let blur_overlay = null;
    if (document.querySelectorAll('.blur-overlay')){
        blur_overlay = document.querySelectorAll('.blur-overlay');
    }

    let profile_container_header_block = null;
    if (document.querySelectorAll('.profile_container_header_block')){
        profile_container_header_block = document.querySelectorAll('.profile_container_header_block');
    }

    let header = null;
    if (document.querySelectorAll('.header')){
        header = document.querySelectorAll('.header');
    }

    let profile_container_favourites_block_comment = null;
    if (document.querySelectorAll('.profile_container_favourites_block_comment')){
        profile_container_favourites_block_comment = document.querySelectorAll('.profile_container_favourites_block_comment');
    }

    let profile_container_header_block_info_flex_vis = null;
    if (document.querySelectorAll('.profile_container_header_block_info_flex_vis')){
        profile_container_header_block_info_flex_vis = document.querySelectorAll('.profile_container_header_block_info_flex_vis');
    }

    let profile_container_header_block_info_flex_alt_block = null;
    if (document.querySelectorAll('.profile_container_header_block_info_flex_alt_block')){
        profile_container_header_block_info_flex_alt_block = document.querySelectorAll('.profile_container_header_block_info_flex_alt_block');
    }

    let prod_element_info = null;
    if (document.querySelectorAll('.prod_element_info')){
        prod_element_info = document.querySelectorAll('.prod_element_info');
    }

    let profile_stats_wrapper_container = null;
    if (document.querySelectorAll('.profile-stats-wrapper-container')){
        profile_stats_wrapper_container = document.querySelectorAll('.profile-stats-wrapper-container');
    }

    let chart_column_wrapper = null;
    if (document.querySelectorAll('.chart-column-wrapper')){
        chart_column_wrapper = document.querySelectorAll('.chart-column-wrapper');
    }

    let h3 = null;
    if (document.querySelectorAll('h3')){
        h3 = document.querySelectorAll('h3');
    }

    let hr = null;
    if (document.querySelectorAll('hr')){
        hr = document.querySelectorAll('hr');
    }

    let new_posts_h4 = null;
    if (document.querySelectorAll('.new_posts_h4')){
        new_posts_h4 = document.querySelectorAll('.new_posts_h4');
    }

    let slider_container_wrapper = null;
    if (document.querySelectorAll('.slider-container-wrapper')){
        slider_container_wrapper = document.querySelectorAll('.slider-container-wrapper');
    }

    let hero_popular_container = null;
    if (document.querySelectorAll('.hero-popular-container')){
        hero_popular_container = document.querySelectorAll('.hero-popular-container');
    }

    let skeleton = null;
    if (document.querySelectorAll('.skeleton')){
        skeleton = document.querySelectorAll('.skeleton');
    }
    
    let post_row_container = null;
    if (document.querySelectorAll('.post-row-container')){
        post_row_container = document.querySelectorAll('.post-row-container');
    }

    let blur_bg = null;
    if (document.querySelectorAll('.blur_bg')){
        blur_bg = document.querySelectorAll('.blur_bg');
    }
    
    let main_characters = null;
    if (document.querySelectorAll('.main_characters')){
        main_characters = document.querySelectorAll('.main_characters');
    }

    let you_container_form = null;
    if (document.querySelectorAll('#you_container_form')){
        you_container_form = document.querySelectorAll('#you_container_form');
    }
  
    let star_rating = null;
    if (document.querySelectorAll('.star-rating')){
        star_rating = document.querySelectorAll('.star-rating');
    }

    let you_container_dop_block = null;
    if (document.querySelectorAll('.you_container_dop_block')){
        you_container_dop_block = document.querySelectorAll('.you_container_dop_block');
    }

    let no_comment_block = null;
    if (document.querySelectorAll('.no_comment_block')){
        no_comment_block = document.querySelectorAll('.no_comment_block');
    }

    if (input.checked != true){ 
        // Светлая тема
        img.src = img.dataset.sun;
        
        if (login_pic != null){
            login_pic.style.filter = 'invert(0)';
        }

        document.body.classList.remove('dark-theme');
        
        for (const element of main_items_background) {
            element.style.backgroundColor = "white";
            element.style.color = "black";
            element.style.border =  "1px solid rgbaa(150, 150, 150, 0.25)";
        }
        
        if (filter != null){
            filter.style.background = "none";
            filter.style.border = "none";
        }

        if (find_by_name != null){
            find_by_name.style.setProperty('--text-color', 'black');
        }

        if (find_by_name2 != null){
            find_by_name2.style.setProperty('--text-color', 'black');
        }

        if (find_by_name2_container != null){
            find_by_name2_container.style.backgroundColor = 'rgb(220, 220, 220)';
        }

        if (catalog != null){
            catalog.style.borderTop = 'none';
        }

        for (const element of new_products_h4){
            element.style.color = "black";
        }

        for (const element of font1) {
            element.style.color = "black";
        }

        for (const element of font2) {
            element.style.color = "black";
        }

        for (const element of textC_gr) {
            element.style.setProperty('--pseudo-bg-color', 'rgb(255, 255, 255)');
        }

        for (const element of filterList_tags) {
            element.style.setProperty('--pseudo-bg-color', 'rgb(255, 255, 255)');
            element.style.setProperty('--pseudo-bg-hover-color', 'rgb(200, 200, 200)');
        }

        for (const element of filterList_tags_checkBoxes) {
            element.style.setProperty('--pseudo-bg-checkbox-color', 'rgb(250, 250, 250)');
            element.style.setProperty('--pseudo-bg-checked-color', 'rgb(30, 30, 30)');
        }

        for (const element of btn_logo) {
            element.style.color = "rgb(0, 0, 0)";
        }
        
        // if (username){
        //     nickname.style.color = "rgb(0, 0, 0)";
        // }
        if (fonts != null){
            for (const element of fonts) {
                element.style.color = 'black';
            }
        }
        if (auth_form_input != null){
            for (const element of auth_form_input) {
                element.style.background = 'rgb(255, 255, 255)';
                element.style.border = '1px solid rgb(220, 220, 220)';
                element.style.color = 'black';
            }
        }
        if (auth_button != null){
            for (const element of auth_button) {
                element.style.background = 'rgb(255, 255, 255)';
                element.style.border = '1px solid rgb(150, 150, 150)';
            }
        }

        if (you_container_dop_block_text != null){
            for (const element of you_container_dop_block_text) {
                element.style.background = 'rgb(200, 200, 200)';
                element.style.border = '1px solid rgb(180, 180, 180)';
                element.style.color = 'rgb(30, 30, 30)';
            }
        }

        if (comments_container != null){
            for (const element of comments_container) {
                element.style.background = 'rgb(200, 200, 200)';
                element.style.border = '1px solid rgb(180, 180, 180)';
                element.style.color = 'rgb(30, 30, 30)';
            }
        }

        for (const element of related_product_link) {
            element.style.color = 'rgb(20, 20, 20)';
            element.style.textShadow = '0 0 10px rgba(255, 255, 255, 0.9), 0 0 20px rgba(255, 255, 255, 0.9), 0 0 30px rgba(255, 255, 255, 0.9)';
        }

        if (main_characters_img_block_fade != null){
            for (const element of main_characters_img_block_fade) {
                element.style.background = 'linear-gradient(to right, rgba(255, 255, 255, 0), rgb(255, 255, 255))';
            }
        }

        if (filter_blocks_grid != null){
            for (const element of filter_blocks_grid) {
                element.style.background = 'rgb(255, 255, 255)';
                element.style.border = '1px solid rgb(150, 150, 150)';
            }
        }

        if (choices__list != null){
            for (const element of choices__list) {
                element.style.backgroundColor = 'rgb(255, 255, 255)';
                element.style.color = 'rgb(30, 30, 30)';
            }
        }

        if (choices__list__single != null){
            for (const element of choices__list__single) {
                element.style.backgroundColor = 'rgb(255, 255, 255)';
                element.style.color = 'rgb(30, 30, 30)';
            }
        }

        if (select_sort != null){
            for (const element of select_sort) {
                element.style.setProperty('--pseudo-list-dropdown-bg', 'rgb(255, 255, 255)');
                element.style.setProperty('--pseudo-list-dropdown-selected', 'rgb(200, 200, 200)');
                element.style.setProperty('--pseudo-list-dropdown-is-highlighted', 'rgb(200, 200, 200)');
                element.style.setProperty('--pseudo-list-dropdown-choices-item-color', 'rgb(30, 30, 30)');
            }
        }

        if (text_fix != null){
            for (const element of text_fix) {
                element.style.color = 'rgb(0, 0, 0)';
            }
        }

        if (all_comments_container != null){
            for (const element of all_comments_container) {
                element.style.setProperty('--pseudo-comment-border-color', 'rgb(205, 205, 205)');
            }
        }

        if (answer != null){
            for (const element of answer) {
                element.style.setProperty('--pseudo-comment-border-color', 'rgb(205, 205, 205)');
            }
        }

        if (blur_overlay != null){
            for (const element of blur_overlay) {
                element.style.setProperty('--psuedo-perescaz-overlay-color', 'rgb(220, 220, 220)');
                element.style.color = 'rgb(40, 40, 40)';
            }
        }
        
        if (profile_container_header_block != null){
            for (const element of profile_container_header_block) {
                element.style.color = 'rgb(30, 30, 30)';
            }
        }

        if (header != null){
            for (const element of header) {
                element.style.border = '0px';
                element.style.borderBottom = '1px solid rgba(150, 150, 150, 0.25)';
            }
        }

        if (profile_container_favourites_block_comment != null){
            for (const element of profile_container_favourites_block_comment) {
                element.style.backgroundColor = 'rgb(255, 255, 255)';
                element.style.border = '1px solid rgb(150, 150, 150)';
                element.style.color = 'rgb(50, 50, 50)';
            }
        }

        if (profile_container_header_block_info_flex_vis != null){
            for (const element of profile_container_header_block_info_flex_vis) {
                element.style.backgroundColor = 'rgb(230, 230, 230)';
            }
        }

        if (profile_container_header_block_info_flex_alt_block != null){
            for (const element of profile_container_header_block_info_flex_alt_block) {
                element.style.backgroundColor = 'rgb(230, 230, 230)';
            }
        }

        if (prod_element_info != null){
            for (const element of prod_element_info) {
                element.style.color = 'rgb(20, 20, 20)';
            }
        }

        if (profile_stats_wrapper_container != null){
            for (const element of profile_stats_wrapper_container) {
                element.style.background = 'rgba(200, 200, 200, 0.3)';
                element.style.color = 'rgb(30, 30, 30)';
            }
        }

        if (chart_column_wrapper != null){
            for (const element of chart_column_wrapper) {
                element.style.color = 'rgb(30, 30, 30)';
            }
        }

        if (h3 != null){
            for (const element of h3) {
                element.style.color = 'rgb(30, 30, 30)';
            }
        }

        if (hr != null){
            for (const element of hr) {
                element.style.color = 'rgb(30, 30, 30)';
            }
        }

        if (dropdown_content_linear_gr != null){
            for (const element of dropdown_content_linear_gr) {
                element.style.setProperty('--pseudo-dropdown-content-linear-gr-background', 'linear-gradient(to bottom, rgba(255, 255, 255, 100%), rgba(255, 255, 255, 0))');
            }
        }

        if (dropdown_content != null){
            for (const element of dropdown_content) {
                element.style.setProperty('--pseudo-dropdown-content-scrollbar-color', 'rgb(150, 150, 150)');
            }
        }

        if (basket != null){
            for (const element of basket) {
                element.style.filter = 'invert(0)';
            }
        }

        for (const element of new_posts_h4) {
            element.style.color = "rgb(50, 50, 50)";
        }

        for (const element of slider_container_wrapper) {
            element.style.background = "inherit";
        }

        for (const element of hero_popular_container) {
            element.style.background = "linear-gradient(to right, rgba(135, 135, 135, 0.75) 30%, rgba(135, 135, 135, 0.55) 100%)";
        }
        
        for (const element of skeleton) {
            element.style.background = "rgb(200, 200, 200)";
        }

        for (const element of post_row_container) {
            element.style.background = "linear-gradient(to right, rgba(120, 120, 120, 0.65) 20%, rgba(120, 120, 120, 0.45) 60%, rgba(120, 120, 120, 0.2) 100%)";
        }

        for (const element of blur_bg) {
            element.style.filter = "blur(10px) brightness(0.75)";
        }

        for (const element of main_characters) {
            element.style.background = "rgb(255, 255, 255)";
        }

        for (const element of you_container_form) {
            element.style.background = "linear-gradient(90deg, rgba(50, 50, 60, 0.2) 0%, rgba(50, 50, 50, 0.2) 35%, rgba(170, 170, 170) 100%)";
        }

        for (const element of star_rating) {
            element.style.color = "rgb(135,135,135)";
        }

        for (const element of you_container_dop_block) {
            element.style.background = "linear-gradient(90deg, rgb(170, 170, 170) 0%, rgba(50, 50, 50, 0.2) 65%, rgba(50, 50, 60, 0.2) 100%)";
        }

        for (const element of no_comment_block) {
            element.style.backgroundColor = "rgb(170, 170, 170)";
        }

        body.style.background = "rgb(220, 220, 220)";

        input.checked = true;
        page_style = 'white';

        favicon.href = window.favicons.light;
    }
    else{
        // Тёмная тема
        img.src = img.dataset.moon;

        if (login_pic != null){
            login_pic.style.filter = 'invert(1)';
        }

        document.body.classList.add('dark-theme');

        for (const element of main_items_background) {
            element.style.backgroundColor = "rgba(30, 30, 30)";
            element.style.color = "rgb(200, 200, 200)";
            element.style.border =  "1px solid rgba(60, 60, 60, 0.25)";
        }

        for (const element of font1) {
            element.style.color = "rgb(200, 200, 200)";
        }

        for (const element of font2) {
            element.style.color = "gray";
        }

        for (const element of textC_gr) {
            element.style.setProperty('--pseudo-bg-color', 'rgb(30, 30, 30)');
        }

        for (const element of filterList_tags) {
            element.style.setProperty('--pseudo-bg-color', 'rgb(30, 30, 30)');
            element.style.setProperty('--pseudo-bg-hover-color', 'rgb(35, 35, 35)');
        }
        
        for (const element of filterList_tags_checkBoxes) {
            element.style.setProperty('--pseudo-bg-checkbox-color', 'rgb(0, 0, 0)');
            element.style.setProperty('--pseudo-bg-checked-color', 'rgb(200, 200, 200)');
        }
        if (filter != null){
            filter.style.background = "none";
            filter.style.border = "none";
        }

        if (find_by_name != null){
            find_by_name.style.setProperty('--text-color', 'rgb(200, 200, 200)');
        }

        if (find_by_name2 != null){
            find_by_name2.style.setProperty('--text-color', 'rgb(200, 200, 200)');
        }

        if (find_by_name2_container != null){
            find_by_name2_container.style.backgroundColor = 'rgb(20, 20, 20)';
        }

        if (catalog != null){
            catalog.style.borderTop = 'none';
        }

        for (const element of new_products_h4){
            element.style.color = "rgb(200, 200, 200)";
        }

        for (const element of btn_logo) {
            element.style.color = "rgb(255, 255, 255)";
        }

        // if (username){
        //     nickname.style.color = "rgb(255, 255, 255)";
        // }
        if (fonts != null){
            for (const element of fonts) {
                element.style.color = 'rgb(200, 200, 200)';
            }
        }
        if (auth_form_input != null){
            for (const element of auth_form_input) {
                element.style.background = 'rgb(60, 60, 60)';
                element.style.border = '1px solid rgb(60, 60, 60)';
                element.style.color = 'rgb(200, 200, 200)';
            }
        }
        if (auth_button != null){
            for (const element of auth_button) {
                element.style.background = 'rgb(60, 60, 60)';
                element.style.border = '1px solid rgb(150, 150, 150)';
            }
        }

        if (you_container_dop_block_text != null){
            for (const element of you_container_dop_block_text) {
                element.style.background = 'rgb(80, 80, 80)';
                element.style.border = '1px solid rgb(80, 80, 80)';
                element.style.color = 'rgb(200, 200, 200)';
            }
        }

        if (comments_container != null){
            for (const element of comments_container) {
                element.style.background = 'rgb(80, 80, 80)';
                element.style.border = '1px solid rgb(120, 120, 120)';
                element.style.color = 'rgb(200, 200, 200)';
            }
        }

        for (const element of related_product_link) {
            element.style.color = 'rgb(200, 200, 200)';
            element.style.textShadow = 'none';
        }

        if (main_characters_img_block_fade != null){
            for (const element of main_characters_img_block_fade) {
                element.style.background = 'linear-gradient(to right, rgba(255, 255, 255, 0), rgb(30, 30, 30))';
            }
        }

        if (filter_blocks_grid != null){
            for (const element of filter_blocks_grid) {
                element.style.background = 'rgb(30, 30, 30)';
                element.style.border = '1px solid rgb(60, 60, 60)';
            }
        }

        if (choices__list != null){
            for (const element of choices__list) {
                element.style.backgroundColor = 'rgb(255, 255, 255)';
                element.style.color = 'rgb(30, 30, 30)';
            }
        }

        if (choices__list__single != null){
            for (const element of choices__list__single) {
                element.style.backgroundColor = 'rgb(30, 30, 30)';
                element.style.color = 'rgb(230, 230, 230)';
            }
        }

        if (select_sort != null){
            for (const element of select_sort) {
                element.style.setProperty('--pseudo-list-dropdown-bg', 'rgb(50, 50, 50)');
                element.style.setProperty('--pseudo-list-dropdown-selected', 'rgb(100, 100, 100)');
                element.style.setProperty('--pseudo-list-dropdown-is-highlighted', 'rgb(100, 100, 100)');
                element.style.setProperty('--pseudo-list-dropdown-choices-item-color', 'rgb(200, 200, 200)');
            }
        }

        if (text_fix != null){
            for (const element of text_fix) {
                element.style.color = 'rgb(200, 200, 200)';
            }
        }

        if (all_comments_container != null){
            for (const element of all_comments_container) {
                element.style.setProperty('--pseudo-comment-border-color', 'rgb(45, 45, 45)');
            }
        }

        if (answer != null){
            for (const element of answer) {
                element.style.setProperty('--pseudo-comment-border-color', 'rgb(45, 45, 45)');
            }
        }

        if (blur_overlay != null){
            for (const element of blur_overlay) {
                element.style.setProperty('--psuedo-perescaz-overlay-color', 'rgb(20, 20, 20)');
                element.style.color = 'rgb(255, 255, 255)';
            }
        }

        if (profile_container_header_block != null){
            for (const element of profile_container_header_block) {
                element.style.color = 'rgb(200, 200, 200)';
            }
        }

        if (header != null){
            for (const element of header) {
                element.style.border = '0px';
                element.style.borderBottom = '1px solid rgba(60, 60, 60, 0.25)';
            }
        }

        if (profile_container_favourites_block_comment != null){
            for (const element of profile_container_favourites_block_comment) {
                element.style.backgroundColor = 'rgb(40, 40, 40)';
                element.style.border = '1px solid rgb(60, 60, 60)';
                element.style.color = 'rgb(200, 200, 200)';
            }
        }

        if (profile_container_header_block_info_flex_vis != null){
            for (const element of profile_container_header_block_info_flex_vis) {
                element.style.backgroundColor = '#1e1e1e';
            }
        }

        if (profile_container_header_block_info_flex_alt_block != null){
            for (const element of profile_container_header_block_info_flex_alt_block) {
                element.style.backgroundColor = '#1e1e1e';
            }
        }

        if (prod_element_info != null){
            for (const element of prod_element_info) {
                element.style.color = 'inherit';
            }
        }

        if (profile_stats_wrapper_container != null){
            for (const element of profile_stats_wrapper_container) {
                element.style.background = '#1e1e1e';
                element.style.color = '';
            }
        }

        if (chart_column_wrapper != null){
            for (const element of chart_column_wrapper) {
                element.style.color = 'inherit';
            }
        }

        if (h3 != null){
            for (const element of h3) {
                element.style.color = 'inherit';
            }
        }

        if (hr != null){
            for (const element of hr) {
                element.style.color = 'inherit';
            }
        }

        if (dropdown_content_linear_gr != null){
            for (const element of dropdown_content_linear_gr) {
                element.style.setProperty('--pseudo-dropdown-content-linear-gr-background', 'linear-gradient(to bottom, rgba(30, 30, 30, 100%), rgba(30, 30, 30, 0))');
            }
        }

        if (dropdown_content != null){
            for (const element of dropdown_content) {
                element.style.setProperty('--pseudo-dropdown-content-scrollbar-color', 'rgb(50, 50, 50)');
            }
        }
        
        if (basket != null){
            for (const element of basket) {
                element.style.filter = 'invert(0.8)';
            }
        }

        for (const element of new_posts_h4) {
            element.style.color = "inherit";
        }

        for (const element of slider_container_wrapper) {
            element.style.background = "#141414";
        }

        for (const element of hero_popular_container) {
            element.style.background = "linear-gradient(to right, rgba(20, 20, 20, 0.95) 30%, rgba(20, 20, 20, 0.75) 100%)";
        }

        for (const element of skeleton) {
            element.style.background = "rgb(31, 31, 31)";
        }

        for (const element of post_row_container) {
            element.style.background = "linear-gradient(to right, rgba(20, 20, 20, 0.98) 20%, rgba(20, 20, 20, 0.85) 60%, rgba(20, 20, 20, 0.4) 100%)";
            element.style.color = '#ffffff';
        }

        for (const element of blur_bg) {
            element.style.filter = "blur(10px) brightness(0.3)";
        }

        for (const element of main_characters) {
            element.style.background = "rgb(30, 30, 30)";
        }

        for (const element of you_container_form) {
            element.style.background = "linear-gradient(90deg, rgba(50, 50, 60, 0.4) 0%, rgb(30, 30, 30) 35%, rgb(30, 30, 30) 100%)";
        }

        for (const element of star_rating) {
            element.style.color = "gray";
        }

        for (const element of you_container_dop_block) {
            element.style.background = "linear-gradient(90deg, rgb(30, 30, 30) 0%, rgb(30, 30, 30) 35%, rgba(50, 50, 60, 0.4) 100%)";
        }

        for (const element of no_comment_block) {
            element.style.backgroundColor = "rgb(170, 170, 170)";
        }

        body.style.background = "rgb(20, 20, 20)";

        input.checked = false;
        page_style = 'black';

        favicon.href = window.favicons.dark;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const formData = new URLSearchParams();
    formData.append('theme_content', page_style);

    //отправляем page_style на сервер
    const api_url = window.location.origin + "/theme/set/";
    fetch(api_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    })
    .then(responce => responce.json())
}

const favicon = document.getElementById('favicon');
document.addEventListener('DOMContentLoaded', function() {
    courent_theme = window.currentTheme;
    username = window.username;

    let login_pic = null;
    if(document.getElementById('login_pic')){
       login_pic = document.getElementById('login_pic');
    }

    // console.log(username);
    // console.log(page_style, courent_theme);
    if (page_style != courent_theme && courent_theme){
        ChangeTheme(username);
    }
    if (page_style == 'black'){
        document.body.classList.add('dark-theme');
        if (login_pic != null){
            login_pic.style.filter = 'invert(1)';
        }
        favicon.href = window.favicons.dark;
    } else {
        document.body.classList.remove('dark-theme');
        if (login_pic != null){
            login_pic.style.filter = 'invert(0)';
        }
        favicon.href = window.favicons.light;
    }
})