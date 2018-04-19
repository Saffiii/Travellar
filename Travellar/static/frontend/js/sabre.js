function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        var token = $("input[name*='csrfmiddlewaretoken']").val();
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", token);
        }
    }
});

$(function () {
    var flights, index, hotels, rentals;

    $.ajax({
        type: "GET",
        url: "/api/sabre",
        success: function (response) {
            //console.log(response)
            flights = response.data.destinations;
            hotels = response.data.hotels;
            rentals = response.data.rentals;
            index = response.data.topDestination.Destinations

            if (window.location.pathname === '/flights') {
                updateFlightsView(flights)
            }

            if (window.location.pathname === '/') {
                updateIndexView(index)
            }

            if (window.location.pathname === '/hotel') {
                updateHotelView(hotels)
            }

            if (window.location.pathname === '/rental') {
                updateRentalView(rentals)
            }
        },
        error: function () {
            console.log('Error')
        }
    });
});


function updateFlightsView(data){
    console.log(data)
    for (var key in data) {

        if (data.hasOwnProperty(key)) {
            if(data[key].DestinationLocation && data[key].LowestFare.Fare) {
                var destination = data[key].DestinationLocation;
                var price = data[key].LowestFare.Fare.toString() + " " + data[key].CurrencyCode;
                // if (key < 8) {
                $('.banners').append("<div class=\"grid_4\">" +
                    "                    <div class=\"banner\">" +
                    "                        <img src= 'static/frontend/img/page2_img1.jpg'  alt=\"\">" +
                    "                        <div class=\"label\">" +
                    "                            <div class=\"title\">" + destination + "</div>" +
                    "                            <div class=\"price\">from<span>" + price + "</span></div>" +
                    "                            <a href=\"#\">LEARN MORE</a>" +
                    "                        </div>" +
                    "                    </div>" +
                    "                </div>");
                // }
            }
        }
    }
}

function updateIndexView(data){
    for (var key in data) {
        let datarow = data[key].Destination;
        let destination;
        let country = datarow.CountryName;

        if (datarow.CityName){
            destination = datarow.CityName
        }
        else if (datarow.MetropolitanAreaName){
            destination = datarow.MetropolitanAreaName
        }
        else{
            destination = datarow.RegionName
        }
        $('.popular').append("<div class=\"grid_4\">" +
            "                    <div class=\"banner\">" +
            "                        <img src= 'static/frontend/img/page2_img1.jpg'  alt=\"\">" +
            "                        <div class=\"label\">" +
            "                            <div class=\"title\">" + destination + "</div>" +
            "                            <div class=\"price\"><span>" + country + "</span></div>" +
            "                            <a href=\"#\">LEARN MORE</a>" +
            "                        </div>" +
            "                    </div>" +
            "                </div>");
        // if(key < 8) {
        //     $('.recommendedbyus').append("<div class=\"grid_4\">" +
        //         "                    <div class=\"banner\">" +
        //         "                        <img src= 'static/frontend/img/page2_img1.jpg'  alt=\"\">" +
        //         "                        <div class=\"label\">" +
        //         "                            <div class=\"title\">" + destination + "</div>" +
        //         "                            <div class=\"price\"><span>" + country + "</span></div>" +
        //         "                            <a href=\"#\">LEARN MORE</a>" +
        //         "                        </div>" +
        //         "                    </div>" +
        //         "                </div>");
        // }
        // else{
        //     $('.popular').append("<div class=\"grid_4\">" +
        //         "                    <div class=\"banner\">" +
        //         "                        <img src= 'static/frontend/img/page2_img1.jpg'  alt=\"\">" +
        //         "                        <div class=\"label\">" +
        //         "                            <div class=\"title\">" + destination + "</div>" +
        //         "                            <div class=\"price\"><span>" + country + "</span></div>" +
        //         "                            <a href=\"#\">LEARN MORE</a>" +
        //         "                        </div>" +
        //         "                    </div>" +
        //         "                </div>");
        // }
    }
}

function updateHotelView(data) {
    for (let key in data) {
        let name = data[key].name;
        let city = data[key].city;
        let country = data[key].country;
        $('.banners').append("<div class=\"grid_4\">" +
            "                    <div class=\"banner\">" +
            "                        <img src= 'static/frontend/img/page2_img1.jpg'  alt=\"\">" +
            "                        <div class=\"label\">" +
            "                            <div class=\"title\">" + name + "</div>" +
            "                            <div class=\"price\"><span>" + city + "</span></div>" +
            "                            <div class=\"price\"><span>" + country + "</span></div>" +
            "                            <a href=\"#\">LEARN MORE</a>" +
            "                        </div>" +
            "                    </div>" +
            "                </div>");
    }
}


function updateRentalView(data) {
    for (let key in data) {
        let company = data[key].company;
        let city = data[key].city;
        let country = data[key].country;
        $('.banners').append("<div class=\"grid_4\">" +
            "                    <div class=\"banner\">" +
            "                        <img src= 'static/frontend/img/page2_img1.jpg'  alt=\"\">" +
            "                        <div class=\"label\">" +
            "                            <div class=\"title\">" + company + "</div>" +
            "                            <div class=\"price\"><span>" + city + "</span></div>" +
            "                            <div class=\"price\"><span>" + country + "</span></div>" +
            "                            <a href=\"#\">LEARN MORE</a>" +
            "                        </div>" +
            "                    </div>" +
            "                </div>");
    }
}
