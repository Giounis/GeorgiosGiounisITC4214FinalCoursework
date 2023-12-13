$(document).ready(function () {
    // Handle category and subcategory interactions
    window.onscroll = function() { myFunction() };

    var header = document.getElementById("sticky-header");
    
    var sticky = header.offsetTop;

    function myFunction() {
        if (window.pageYOffset > sticky) {
            header.classList.add("sticky");
        } else {
            header.classList.remove("sticky");
        }
    }

    $('body').on('mouseenter', '.category-list', function () {
        if (!$(this).hasClass('active')) {
            $(this).find('.subcategory-list').show();
        }
    }).on('mouseleave', '.category-list', function () {
        if (!$(this).hasClass('active')) {
            $(this).find('.subcategory-list').hide();
        }
    });

    $('.category-list a').click(function (e) {
        e.preventDefault();

        $('.category-list').removeClass('active');
        $(this).closest('.category-list').addClass('active');
        $('.category-list:not(.active) .subcategory-list').hide();

        window.location.href = $(this).attr('href');
    });
    
});
