$(document).ready(function () {
    var productForm = $('.form-product-ajax');

    productForm.submit(function (event) {
        event.preventDefault();
        // console.log('form is default')
        var thisForm = $(this);
        // var actionEndPoint = thisForm.attr("action");  // API EndPoint
        var actionEndPoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
            url: actionEndPoint,
            method: httpMethod,
            data: formData,
            success: function (data) {
                var submitSpan = thisForm.find(".submit-span");
                if (data.added){
                    submitSpan.html("<button type=\'submit\' class=\'btn btn-sm btn-outline-danger\'>Remove</button>")
                }
                else {
                    submitSpan.html("<button type=\'submit\' class=\'btn btn-lg btn-outline-success\'>Add to Cart</button>")
                }
                var cartCount = $(".cart-count");
                cartCount.text(data.cartItemCount);
                var currentPath = window.location.href;
                if (currentPath.indexOf("cart") != -1) {
                    refreshCart()
                }
            },
            error: function (errorData) {
                console.log("error");
                console.log(errorData);
            }
        })
    });

    function refreshCart() {
        // console.log('current cart');
        var cartTable = $(".cart-table");
        var cartBody = cartTable.find(".cart-body");
        // cartBody.html("<h1>CHANGED</h1>");
        var ProductsRow = cartBody.find(".cart-product");
        var currentUrl = window.location.href;

        var refreshCartUrl = 'api/cart/';
        var refreshCartMethod = "GET";
        var data = {};

        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function (data) {
                console.log("success");
                console.log(data);
                if (data.products.length > 0) {
                    ProductsRow.html("");
                    let i = 1;
                    $.each(data.products, function(index, value){
                        cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td>" + value.name + "</td><td>" + value.price + "</td></tr>");
                        i++
                    });
                    cartBody.find(".cart-subtotal").text(data.subtotal);
                    cartBody.find(".cart-total").text(data.total)
                }
                else {
                    window.location.href = currentUrl
                }
            },
            error: function (errorData) {
                console.log("error");
                console.log(errorData)
            }
        })
    }
});
