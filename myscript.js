$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})

$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})


    < script src = "https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js" ></ >
        <script>
            $(document).ready(function() {
                $('.remove-cart').click(function () {
                    var id = $(this).attr("pid").toString();
                    var eml = this;
                    $.ajax({
                        type: "GET",
                        url: "/removecart/",
                        data: {
                            prod_id: id
                        },
                        success: function (data) {
                            // Update subtotal and total amount in the DOM
                            $("#amount").text(data.amount);  // Update to reflect the new subtotal
                            $("#totalamount").text(data.totalamount);  // Update to reflect the new total amount

                            // Optional: Remove the cart item's HTML element from the page
                            $(eml).closest(".cart-item").remove();  // Assuming your HTML structure; adjust as necessary
                        },
                        error: function (error) {
                            console.log(error);
                            alert("An error occurred. Please try again.");
                        }
                    });
                });
});
        </script>


$('.plus-wishlist').click(function () {
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/pluswishlist",
        data: {
            prod_id: id
        },
        success: function (data) {
            //alert(data.message)
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})


$('.minus-wishlist').click(function () {
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: {
            prod_id: id
        },
        success: function (data) {
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})