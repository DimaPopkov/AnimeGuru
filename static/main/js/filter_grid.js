let grid = 'block';

function UpdateGrid(){
    type = grid;

    let blockGridButton = document.getElementById('block');
    let big_blockGridButton = document.getElementById('big_block');
    let lineGridButton = document.getElementById('line');

    let catalog = document.getElementById('products_catalog');
    let block_img = document.querySelectorAll('.prod_element_pic_lock');
    let block_container = document.querySelectorAll('.prod_element');
    let block_description = document.querySelectorAll('.hidden_description');

    if(type == 'block'){
        blockGridButton.classList.add('active');
        big_blockGridButton.classList.remove('active');
        lineGridButton.classList.remove('active');

        catalog.style.gridTemplateColumns = '175px 175px 175px 175px 175px';
        for(const element of block_img){
            element.style.width = 'auto';
            element.style.height = '245px';
        }
        for(const element of block_container){
            element.style.flexDirection = 'column';
        }
        for(const element of block_description){
            element.classList.add('hidden');
        }
    }
    if(type == 'big_block'){
        blockGridButton.classList.remove('active');
        big_blockGridButton.classList.add('active');
        lineGridButton.classList.remove('active');

        catalog.style.gridTemplateColumns = '301.67px 301.67px 301.67px';
        for(const element of block_img){
            element.style.width = 'auto';
            element.style.height = '400px';
        }
        for(const element of block_container){
            element.style.flexDirection = 'column';
        }
        for(const element of block_description){
            element.classList.add('hidden');
        }
    }
    if(type == 'line'){
        blockGridButton.classList.remove('active');
        big_blockGridButton.classList.remove('active');
        lineGridButton.classList.add('active');

        catalog.style.gridTemplateColumns = '935px';
        for(const element of block_img){
            element.style.width = '175px';
            element.style.height = '245px';
        }
        for(const element of block_container){
            element.style.flexDirection = 'row';
            element.style.columnGap = '10px';
        }
        for(const element of block_description){
            element.classList.remove('hidden');
        }
    }
}

function ChangeGrid(type){
    let blockGridButton = document.getElementById('block');
    let big_blockGridButton = document.getElementById('big_block');
    let lineGridButton = document.getElementById('line');

    let catalog = document.getElementById('products_catalog');
    let block_img = document.querySelectorAll('.prod_element_pic_lock');
    let block_container = document.querySelectorAll('.prod_element');
    let block_description = document.querySelectorAll('.hidden_description');

    if(type == 'block'){
        blockGridButton.classList.add('active');
        big_blockGridButton.classList.remove('active');
        lineGridButton.classList.remove('active');

        catalog.style.gridTemplateColumns = '175px 175px 175px 175px 175px';
        for(const element of block_img){
            element.style.width = 'auto';
            element.style.height = '245px';
        }
        for(const element of block_container){
            element.style.flexDirection = 'column';
        }
        for(const element of block_description){
            element.classList.add('hidden');
        }
    }
    if(type == 'big_block'){
        blockGridButton.classList.remove('active');
        big_blockGridButton.classList.add('active');
        lineGridButton.classList.remove('active');

        catalog.style.gridTemplateColumns = '301.67px 301.67px 301.67px';
        for(const element of block_img){
            element.style.width = 'auto';
            element.style.height = '400px';
        }
        for(const element of block_container){
            element.style.flexDirection = 'column';
        }
        for(const element of block_description){
            element.classList.add('hidden');
        }
    }
    if(type == 'line'){
        blockGridButton.classList.remove('active');
        big_blockGridButton.classList.remove('active');
        lineGridButton.classList.add('active');

        catalog.style.gridTemplateColumns = '935px';
        for(const element of block_img){
            element.style.width = '175px';
            element.style.height = '245px';
        }
        for(const element of block_container){
            element.style.flexDirection = 'row';
            element.style.columnGap = '10px';
        }
        for(const element of block_description){
            element.classList.remove('hidden');
        }
    }
    grid = type;
}