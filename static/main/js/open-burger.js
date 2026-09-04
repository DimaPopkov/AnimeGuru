function OpenBurger() {
    let menu = document.getElementById('burger-menu-block');

    if (menu.style.transform  == 'translateX(0px)') {
        menu.style.transform = 'translateX(100%)';
    } else {
        menu.style.transform = 'translateX(0px)';
    }
}