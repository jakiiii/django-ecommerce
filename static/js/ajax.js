$(document).ready(function () {
    var productForm = $('.form-product-ajax')

    productForm.submit(function (event) {
        event.preventDefault()
        // console.log('form is default')
        var thisForm = $(this)
        var actionEndPoint = thisForm.attr("action");
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
                var cartCount = $(".cart-count")
                cartCount.text(data.cartItemCount)
            },
            error: function (errorData) {
                console.log("error");
                console.log(errorData);
            }
        })
    })
})
