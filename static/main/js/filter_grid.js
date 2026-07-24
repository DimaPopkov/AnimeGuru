let grid = 'block';

function UpdateGrid(){
    let blockGridButton = document.getElementById('block');
    let big_blockGridButton = document.getElementById('big_block');
    let lineGridButton = document.getElementById('line');
    let catalog = document.getElementById('products_catalog');

    if (!catalog) return;

    // Синхронизируем активные классы на кнопках
    blockGridButton?.classList.toggle('active', grid === 'block');
    big_blockGridButton?.classList.toggle('active', grid === 'big_block');
    lineGridButton?.classList.toggle('active', grid === 'line');

    // Обновляем классы режимов на самом каталоге
    catalog.classList.remove('block', 'big_block', 'line');
    catalog.classList.add(grid);

    // Управляем колонками грида в зависимости от режима
    if (grid === 'block') {
        catalog.style.gridTemplateColumns = 'repeat(auto-fit, minmax(min(100%, 120px), 1fr))';
    } else if (grid === 'big_block') {
        catalog.style.gridTemplateColumns = 'repeat(auto-fit, minmax(min(100%, 200px), 1fr))';
    } else if (grid === 'line') {
        catalog.style.gridTemplateColumns = 'repeat(auto-fit, minmax(min(100%, 700px), 1fr))';
    }

    // Если на странице уже есть отрендеренные продукты, обновляем их стили под новый режим
    const block_img = catalog.querySelectorAll('.prod_element_pic_lock');
    const block_container = catalog.querySelectorAll('.prod_element');
    const block_description = catalog.querySelectorAll('.hidden_description');

    const isLine = grid === 'line';

    // Массово применяем стили ко всем текущим карточкам
    block_img.forEach(el => {
        el.style.width = isLine ? '175px' : 'auto';
        el.style.height = 'auto';
    });

    block_container.forEach(el => {
        el.style.flexDirection = isLine ? 'row' : 'column';
        el.style.columnGap = isLine ? '20px' : '';
        el.classList.toggle('line-mode', isLine);
    });

    block_description.forEach(el => {
        el.classList.toggle('hidden', !isLine);
    });
}

// Функция вызывается при клике на кнопки переключения режимов
function ChangeGrid(type){
    grid = type; // Перезаписываем глобальный режим
    UpdateGrid(); // Передаем всю работу по обновлению интерфейса в UpdateGrid
}