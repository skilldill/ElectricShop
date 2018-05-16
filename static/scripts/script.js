 $(function(){
    'use strict';	
    // инициализация плагина
    $.jqCart({
            buttons: '.add_item',
            handler: './setorder',
            cartLabel: '.label-place',
            visibleLabel: true,
            openByAdding: false,
            currency: '₽'
    });	
    // Пример с дополнительными методами
    $('#open').click(function(){
        $.jqCart('openCart'); // открыть корзину
    });
    $('#clear').click(function(){
        $.jqCart('clearCart'); // очистить корзину
    });	
});

