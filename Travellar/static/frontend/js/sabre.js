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
    var flights, index;

    $.ajax({
        type: "GET",
        url: "/api/sabre",
        success: function (response) {
            //console.log(response)
            flights = response.data.destinations;
            index = response.data.topDestination.Destinations
            console.log(flights)
            console.log(index)

            if (window.location.pathname === '/flights') {
                updateFlightsView(flights)
            }

            if (window.location.pathname === '/') {
                updateIndexView(index)
            }


            // for (var key in response.data.Destinations) {
            //     //console.log(response.data.Destinations[key].Destination)
            //     var datarow = response.data.Destinations[key].Destination
            //     if (datarow.CityName){
            //         console.log(datarow.CityName)
            //     }
            //     else if (datarow.MetropolitanAreaName){
            //         console.log(datarow.MetropolitanAreaName)
            //     }
            //     else{
            //         console.log(datarow.RegionName)
            //     }
            // }
        },
        error: function () {
            console.log('Error')
        }
    });
});


function updateFlightsView(data){
    $('.banners').append("<div class=\"grid_4\">" +
        "                    <div class=\"banner\">" +
        "                        <img src= 'static/frontend/img/page2_img1.jpg'  alt=\"\">" +
        "                        <div class=\"label\">" +
        "                            <div class=\"title\">"+data['0'].DestinationLocation+"</div>" +
        "                            <div class=\"price\">from<span>$ 1.200</span></div>" +
        "                            <a href=\"#\">LEARN MORE</a>" +
        "                        </div>" +
        "                    </div>" +
        "                </div>");
}

function updateIndexView(){

}
