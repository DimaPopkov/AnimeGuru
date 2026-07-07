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

        catalog.style.gridTemplateColumns = 'repeat(auto-fit, minmax(min(100%, 120px), 1fr))';
        for(const element of block_img){
            element.style.width = 'auto';
            element.style.height = 'auto';
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

        catalog.style.gridTemplateColumns = 'repeat(auto-fit, minmax(min(100%, 200px), 1fr))';
        for(const element of block_img){
            element.style.width = 'auto';
            element.style.height = 'auto';
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

        catalog.style.gridTemplateColumns = 'repeat(auto-fit, minmax(min(100%, 700px), 1fr))';
        for(const element of block_img){
            element.style.width = '175px';
            element.style.height = 'auto';
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

    blockGridButton.classList.toggle('active', type === 'block');
    big_blockGridButton.classList.toggle('active', type === 'big_block');
    lineGridButton.classList.toggle('active', type === 'line');

    if(type == 'block'){
        catalog.style.gridTemplateColumns = 'repeat(auto-fit, minmax(min(100%, 120px), 1fr))';
        for(const element of block_img){ element.style.width = 'auto'; element.style.height = 'auto'; }
        for(const element of block_container){ 
            element.style.flexDirection = 'column'; 
            element.classList.remove('line-mode'); // Убираем режим линии
        }
        for(const element of block_description){ element.classList.add('hidden'); }
    }
    
    if(type == 'big_block'){
        catalog.style.gridTemplateColumns = 'repeat(auto-fit, minmax(min(100%, 200px), 1fr))';
        for(const element of block_img){ element.style.width = 'auto'; element.style.height = 'auto'; }
        for(const element of block_container){ 
            element.style.flexDirection = 'column'; 
            element.classList.remove('line-mode'); // Убираем режим линии
        }
        for(const element of block_description){ element.classList.add('hidden'); }
    }
    
    if(type == 'line'){
        catalog.style.gridTemplateColumns = 'repeat(auto-fit, minmax(min(100%, 700px), 1fr))';
        for(const element of block_img){ element.style.width = '175px'; element.style.height = 'auto'; }
        for(const element of block_container){ 
            element.style.flexDirection = 'row'; 
            element.style.columnGap = '20px'; // Расстояние от картинки до текста
            element.classList.add('line-mode'); // ВКЛЮЧАЕМ режим линии для CSS
        }
        for(const element of block_description){ element.classList.remove('hidden'); }
    }
    grid = type;
}