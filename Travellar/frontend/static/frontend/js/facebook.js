var access;
var verified;
window.fbAsyncInit = function () {
    FB.init({
        appId: '148030899128651', // Set YOUR APP ID
        status: true, // check login status
        cookie: true, // enable cookies to allow the server to access the session
        xfbml: true  // parse XFBML
    });

    FB.Event.subscribe('auth.authResponseChange', function (response) {
        if (response.status === 'connected') {
            //SUCCESS
            access = response.authResponse.accessToken;
            verified = true;

            $("#facebook-log").remove();
            $(".sf-menu").append("\<li id=\"facebook-log\"\>\<\/li\>");
            // $("#fb-login").hide();
            $("#facebook-log").append("\<a id=\"fb-logout\" onclick=\"Logout()\"\>Facebook Logout\<\/a\>");
            console.log('subscribe-verified')
        } else if (response.status === 'not_authorized') {
            //FAILED
            verified = false;
            console.log('subscribe-NOTverified')
        } else {
            //UNKNOWN ERROR
            verified = false;
            console.log('subscribe-NOTverified')
        }
    });
    FB.Event.subscribe('auth.login', function (response) {
        console.log("login_event");
        console.log(response.authResponse.accessToken);
        access = response.authResponse.accessToken;
        getUserInfo(access)


    });

    FB.getLoginStatus(function(response) {
        console.log('getLoginSatatus')
        if (response.status === 'connected') {}
        else{getUserInfo(access)}

    } );

};


function Login() {
    FB.login(function (response) {
        if (response.authResponse) {
            access = response.authResponse.accessToken;
        } else {
            console.log('User cancelled login or did not fully authorize.');
        }
    }, {scope: 'email,user_tagged_places'});
}

function getUserInfo(access) {
    console.log('getUserInfo')
    FB.api('/me?fields=email,link,name', function (response) {
        if(verified) {
            console.log('getUserInfo-verified')
            getRecommendation(access, response.id, response.email, response.name, true);
        }
        else{
            console.log('getUserInfo-NOTverified')
            getRecommendation(access, 0, null, null, false);
        }
    });
}

function getPhoto() {
    FB.api('/me/picture?type=normal', function (response) {
        var str = "<br/><b>Pic</b> : <img src='" + response.data.url + "'/>";
    });
}


function getCheckIns(access, id, email, name) {
    console.log('getCheckins...')
    let facebookGraphURL = 'https://graph.facebook.com/'+id+'?access_token='+access;
    $.ajax({
        type: "GET",
        url: facebookGraphURL,
        dataType: 'jsonp',
        success: function(response) {
            FB.api("/me?fields=tagged_places", function (response) {
                let postdata = {'place': response.tagged_places.data, 'id':response.id, 'email':email, 'name':name}
                $.ajax({
                    url: '/api/als',
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify(postdata),
                    type: 'POST',
                    success: function(response) {
                        if (window.location.pathname === '/recommendations') {
                            updatePersonalRecommendationsView(response.data)
                        }
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            });
        },
        error: function(err) {
        }
    })
}


function Logout() {
    FB.logout(function () {
        document.location.reload();
    });
}

// Load the SDK asynchronously
(function (d) {
    let js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
    if (d.getElementById(id)) {
        return;
    }
    js = d.createElement('script');
    js.id = id;
    js.async = true;
    js.src = "//connect.facebook.net/en_US/all.js";
    ref.parentNode.insertBefore(js, ref);
}(document));


function getRecommendation(access, id, email, name, flag) {
    console.log('getrecco')
    let recommendations;

    if (window.location.pathname === '/recommendations') {
        if (flag === true) {
            console.log('getting checkin...')
            getCheckIns(access, id, email, name)
        }
        if (flag === false) {
            console.log('NOT getting checkin...')
            $.ajax({
                type: "GET",
                url: "/api/sabre",
                success: function (response) {
                    if (window.location.pathname === '/recommendations') {
                        recommendations = response.data.topRecommendations.Destinations;
                        console.log(verified)
                        updateGuestRecommendationsView(recommendations)
                    }
                },
                error: function () {
                    console.log('Error')
                }
            });
        }
    }
}

function updateGuestRecommendationsView(data) {
    let randomIndex = [];
    while(randomIndex.length < 8){
        let randomnumber = Math.floor(Math.random()*50) + 1;
        if(randomIndex.indexOf(randomnumber) > -1) continue;
        randomIndex[randomIndex.length] = randomnumber;
    }
    console.log(randomIndex);
    for (let i = 0; i < randomIndex.length; i++) {
        let key = randomIndex[i];
        let destination, country, datarow;
        if(data[key]) {
            console.log(data[key])
            if ('Destination' in data[key]) {datarow = data[key].Destination;}
            if ('CountryName' in datarow) {country = datarow.CountryName}

            if (datarow.CityName){destination = datarow.CityName}
            else if (datarow.MetropolitanAreaName){destination = datarow.MetropolitanAreaName}
            else{destination = datarow.RegionName}

            $('.banners').append("<div class=\"grid_4\">" +
                "                    <div class=\"banner\">" +
                "                        <img src= 'static/frontend/img/page2_img1.jpg'  alt=\"\">" +
                "                        <div class=\"label\">" +
                "                            <div class=\"title\">" + destination + "</div>" +
                "                            <div class=\"price\"><span>" + country + "</span></div>" +
                "                            <a href=\"#\">LEARN MORE</a>" +
                "                        </div>" +
                "                    </div>" +
                "                </div>");
        }

    }
}

function updatePersonalRecommendationsView(data) {
    $( "div" ).remove( ".banners" );
    $('#recommendationscontainer').append("<div class=\"banners\">" +
        "                <div class=\"recommendations\">" +
        "                    <div class=\"title\">PERSONAL RECOMMENDATIONS FOR YOU ...</div>" +
        "                </div>" +
        "            </div>");
    for (let i = 0; i < data.length; i++) {
        console.log(data[i]);
        let name = data[i].name;
        let country = data[i].country;
        let state = data[i].state;
        let countrystate="";


        if(country !== "N/A"){countrystate = country;}
        else if (state !== "N/A"){countrystate = state;}
        else{countrystate="-"}

        if (data[i].name) {
            $('.banners').append("<div class=\"grid_4\">" +
                "                    <div class=\"banner\">" +
                "                        <img src= 'static/frontend/img/page2_img1.jpg'  alt=\"\">" +
                "                        <div class=\"label\">" +
                "                            <div class=\"title\">" + name + "</div>" +
                "                            <div class=\"price\"><span>" + countrystate + "</span></div>" +
                "                            <a href=\"#\">LEARN MORE</a>" +
                "                        </div>" +
                "                    </div>" +
                "                </div>");
        }
    }
}
