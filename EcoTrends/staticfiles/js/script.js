$(document).ready(function(){
    $('.category-list').hover(function(){
        $(this).find('.subcategory-list').toggle();
    });

    $('.category-list').click(function(){
        window.location.href = $(this).find('a').attr('href');
    });
});