$(document).ready(function () {
    $('#submit_article_comment').click(function () {
        let comment = document.getElementById('article_comment_text').value;
        let parentId = document.getElementById('article_comment_parent_id').value;
        let articleId = document.getElementById('article_comment_id').value;

        let csrf_Token = $('input[name="csrfmiddlewaretoken"]').val();
        $.post('/articles/add-article-comment', {
            csrfmiddlewaretoken: csrf_Token,
            article_comment: comment,
            article_id: articleId,
            parent_id: parentId
        }).then(res => {
            $('#article_comments_area').html(res);
            $('#article_comment_text').val('');
            $('#article_comment_parent_id').val('');

            if (parentId !== null && parentId !== '') {
                document.getElementById('single_article_comment_box_' + parentId).scrollIntoView({behavior: "smooth"});
            } else {
                document.getElementById('article_comments_area').scrollIntoView({behavior: "smooth"});
            }
        });
    });
});

function fillParentId(parentId) {
    $('#article_comment_parent_id').val(parentId);
    document.getElementById('article_comment_form').scrollIntoView({behavior: "smooth"});

}


function filterProducts() {
    const filterPrice = $('#sl2').val();
    const first_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];
    $('#start_price').val(first_price);
    $('#end_price').val(end_price);
    $('#filter_form').submit();
}

function fillPage(page) {
    $('#page').val(page);
    $('#filter_form').submit();
}

function ShowLargeImage(imageSrc) {
    $('#main_image').attr('src', imageSrc);
    $('#show_large_image_modal').attr('href', imageSrc);
}


function addProductToOrder(productId) {
    const productCount = $('#product_count').val()
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount).then(res => {
        Swal.fire({
            title: 'اعلان',
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: '#3085d6',
            confirmButtonText: res.confirm_button_text
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_auth') {
                window.location.href = '/login';
            }
        })
    });
}

function removeOrderDetail(detailId) {
    $.get('/user/remove-order-detail?detail_id=' + detailId).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}

function changeOrderDetailCount(detailId, state) {
    $.get('/user/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}


$(document).ready(function () {
    $('#submit_comment').click(function () {
        let productComment = document.getElementById('product_comment_text').value;
        let commentParent = document.getElementById('product_comment_parent_id').value;
        let productId = document.getElementById('product_comment_id').value;

        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        $.post('/products/add-product-comment', {
            csrfmiddlewaretoken: csrfToken,
            product_id: productId,
            product_comment: productComment,
            parent_id: commentParent

        }).then(res => {
            $('#product_comments_area').html(res);
            $('#product_comment_text').val('');
            $('#product_comment_parent_id').val('');
            console.log(res);
            if (commentParent !== null && commentParent !== '') {
                document.getElementById('single_product_comment_box_' + commentParent).scrollIntoView({behavior: "smooth"});
            } else {
                document.getElementById('product_comments_area').scrollIntoView({behavior: "smooth"});
            }

        });
    });
});


function fillProductParent(productParentId) {
    document.getElementById('product_comment_parent_id').value = productParentId;
    document.getElementById('product_comment_form').scrollIntoView({behavior: "smooth"});
}



