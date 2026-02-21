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
    let btn_logo = document.getElementById('btn_logo');
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


    let you_container_dop = null;
    if (document.querySelectorAll('.you_container_dop')){
        you_container_dop = document.querySelectorAll('.you_container_dop');
    }

    let you_container_text_container = null;
    if (document.querySelectorAll('.you_container_text_container')){
        you_container_text_container = document.querySelectorAll('.you_container_text_container');
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


    if (input.checked != true){ 
        // Светлая тема
        img.src = img.dataset.sun;     
        
        for (const element of main_items_background) {
            element.style.backgroundColor = "white";
            element.style.color = "black";
            element.style.border =  "1px solid rgb(150, 150, 150)";
        }

        for (const element of font1) {
            element.style.color = "black";
        }

        for (const element of font2) {
            element.style.color = "black";
        }

        for (const element of textC_gr) {
            element.style.setProperty('--pseudo-bg-color', 'linear-gradient(transparent, rgb(30, 30, 30))');
        }

        for (const element of filterList_tags) {
            element.style.setProperty('--pseudo-bg-color', 'rgb(255, 255, 255)');
            element.style.setProperty('--pseudo-bg-hover-color', 'rgb(200, 200, 200)');
        }

        for (const element of filterList_tags_checkBoxes) {
            element.style.setProperty('--pseudo-bg-checkbox-color', 'rgb(220, 220, 220)');
            element.style.setProperty('--pseudo-bg-checked-color', 'rgb(30, 30, 30)');
        }

        btn_logo.style.color = "rgb(0, 0, 0)";
        if (username){
            nickname.style.color = "rgb(0, 0, 0)";
        }
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

        if (you_container_dop != null){
            for (const element of you_container_dop) {
                element.style.background = 'rgb(240, 240, 240)';
                element.style.border = '1px solid rgb(180, 180, 180)';
            }
        }

        if (you_container_text_container != null){
            for (const element of you_container_text_container) {
                element.style.background = 'rgb(200, 200, 200)';
                element.style.border = '1px solid rgb(180, 180, 180)';
                element.style.color = 'rgb(30, 30, 30)';
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

        if (main_characters_img_block_fade != null){
            for (const element of main_characters_img_block_fade) {
                element.style.background = 'linear-gradient(to right, rgba(255, 255, 255, 0), rgb(255, 255, 255))';
            }
        }

        body.style.background = "rgb(220, 220, 220)";

        input.checked = true;
        page_style = 'white';
    }
    else{
        // Тёмная тема
        img.src = img.dataset.moon;

        for (const element of main_items_background) {
            element.style.backgroundColor = "rgba(30, 30, 30)";
            element.style.color = "rgb(200, 200, 200)";
            element.style.border =  "1px solid rgb(60, 60, 60)";
        }

        for (const element of font1) {
            element.style.color = "rgb(200, 200, 200)";
        }

        for (const element of font2) {
            element.style.color = "gray";
        }

        for (const element of textC_gr) {
            element.style.setProperty('--pseudo-bg-color', 'linear-gradient(transparent, rgb(30, 30, 30))');
        }

        for (const element of filterList_tags) {
            element.style.setProperty('--pseudo-bg-color', 'rgb(30, 30, 30)');
            element.style.setProperty('--pseudo-bg-hover-color', 'rgb(35, 35, 35)');
        }
        
        for (const element of filterList_tags_checkBoxes) {
            element.style.setProperty('--pseudo-bg-checkbox-color', 'rgb(0, 0, 0)');
            element.style.setProperty('--pseudo-bg-checked-color', 'rgb(200, 200, 200)');
        }

        btn_logo.style.color = "rgb(255, 255, 255)";
        if (username){
            nickname.style.color = "rgb(255, 255, 255)";
        }
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

        if (you_container_dop != null){
            for (const element of you_container_dop) {
                element.style.background = 'rgb(50, 50, 50)';
                element.style.border = '1px solid rgb(80, 80, 80)';
            }
        }

        if (you_container_text_container != null){
            for (const element of you_container_text_container) {
                element.style.background = 'rgb(80, 80, 80)';
                element.style.border = '1px solid rgb(80, 80, 80)';
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
                element.style.border = '1px solid rgb(80, 80, 80)';
                element.style.color = 'rgb(200, 200, 200)';
            }
        }

        if (main_characters_img_block_fade != null){
            for (const element of main_characters_img_block_fade) {
                element.style.background = 'linear-gradient(to right, rgba(255, 255, 255, 0), rgb(30, 30, 30))';
            }
        }

        body.style.background = "rgb(20, 20, 20)";

        input.checked = false;
        page_style = 'black';
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
    const api_url = "http://127.0.0.1:8000/theme/set/";
    fetch(api_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    })
    .then(responce => responce.json())
    .then(responce => {
        console.log(responce)
    })
}

document.addEventListener('DOMContentLoaded', function() {
    courent_theme = window.currentTheme;
    username = window.username;
    console.log(username);
    console.log(page_style, courent_theme);
    if (page_style != courent_theme && courent_theme){
        ChangeTheme(username);
    }
})