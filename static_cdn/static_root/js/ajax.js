$(document).ready(function () {
    // Contact Form Handler
    let contactForm = $(".contact-form");
    let contactFormMethod = contactForm.attr("method");
    let contactFormEndpoint = contactForm.attr("action");


    function displaySubmitting(submitBtn, defaultText, doSubmit) {
        if (doSubmit) {
            submitBtn.addClass("disabled");
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Submitting");
        } else {
            submitBtn.removeClass("disabled");
            submitBtn.html(defaultText)
        }
    }

    contactForm.submit(function (event) {
        event.preventDefault()
        let contactFormData = contactForm.serialize();
        let thisForm = $(this);
        let contactFormSubmitBtn = contactForm.find("[name='submit']");
        let contactFormSubmitBtnTxt = contactFormSubmitBtn.text();

        displaySubmitting(contactFormSubmitBtn, "", true);
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function (data) {
                contactForm[0].reset();
                $.confirm({
                    theme: 'dark',
                    title: 'Success',
                    content: data.message,
                });
                setTimeout(function () {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false);
                }, 500)
            },
            error: function (error) {
                console.log("error");
                console.log(error.responseJSON);
                let jsonData = error.responseJSON;
                let msg = "";

                $.each(jsonData, function (key, value) {
                    msg += key + ": " + value[0].message + "<br/>"
                });

                $.confirm({
                    theme: 'material',  // supervan
                    title: 'Oops!',
                    content: msg,
                });

                setTimeout(function () {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false);
                }, 500)
            }
        })
    });


    // Ajax Search
    let searchForm = $(".search-form");
    let searchInput = searchForm.find("[name='q']");
    let typingTimer;
    let typingInterval = 1500;  // .5s

    let searchBtn = searchForm.find("[name='submit']");

    searchInput.keyup(function (event) {
        // key realised
        clearTimeout(typingTimer);
        typingTimer = setTimeout(performSearch, typingInterval)
    });

    searchInput.keydown(function (event) {
        // key pressed
        clearTimeout(typingTimer);
    });
    
    function searching() {
        searchBtn.addClass("disabled");
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i>");
    }

    function performSearch() {
        searching();
        let query = searchInput.val();
        setTimeout(function () {
            window.location.href='/search/?q=' + query
        }, 500)
    }



    // Cart Add / Remove Products
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
                    submitSpan.html("<button type=\'submit\' class=\'btn btn-outline-danger\'>Remove</button>")
                }
                else {
                    submitSpan.html("<button type=\'submit\' class=\'btn btn-outline-success\'>Add to Cart</button>")
                }
                var cartCount = $(".cart-count");
                cartCount.text(data.cartItemCount);
                var currentPath = window.location.href;
                if (currentPath.indexOf("cart") != -1) {
                    refreshCart()
                }
            },
            error: function (errorData) {
                $.confirm({
                    theme: 'light',
                    title: 'Oops!',
                    content: 'An error occurred!',
                });
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
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form");
                if (data.products.length > 0) {
                    ProductsRow.html("");
                    let i = data.products.length;
                    $.each(data.products, function(index, value){
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone();
                        newCartItemRemove.css("display", "block");
                        // newCartItemRemove.removeClass("hidden-class");
                        newCartItemRemove.find(".cart-item-product-id").val(value.id);
                        cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a></td><td>" + value.price + "</td>" +
                            "<td class=\"text-center\" width=\"200px;\">" + newCartItemRemove.html() + "</td></tr>");
                        i--
                    });
                    cartBody.find(".cart-subtotal").text(data.subtotal);
                    cartBody.find(".cart-total").text(data.total)
                }
                else {
                    window.location.href = currentUrl
                }
            },
            error: function (errorData) {
                $.confirm({
                    theme: 'light',
                    title: 'Oops!',
                    content: 'An error occurred!',
                });
            }
        })
    }
});
