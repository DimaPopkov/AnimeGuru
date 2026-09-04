function OpenBurger() {
    let menu = document.getElementById('burger-menu-block');

    if (menu.style.marginLeft == '0px') {
        menu.style.marginLeft = '100vw';
    } else {
        menu.style.marginLeft = '0px';
    }
}