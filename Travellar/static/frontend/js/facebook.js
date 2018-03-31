var access;
window.fbAsyncInit = function() {
    FB.init({
        appId      : '148030899128651', // Set YOUR APP ID
        status     : true, // check login status
        cookie     : true, // enable cookies to allow the server to access the session
        xfbml      : true  // parse XFBML
    });

    FB.Event.subscribe('auth.authResponseChange', function(response) {
        if (response.status === 'connected') {
            //SUCCESS
            document.getElementById("message").innerHTML +=  "<br>Connected to Facebook";
            getUserInfo();
        } else if (response.status === 'not_authorized') {
            //FAILED
            document.getElementById("message").innerHTML +=  "<br>Failed to Connect";
        } else {
            //UNKNOWN ERROR
            document.getElementById("message").innerHTML +=  "<br>Logged Out";
        }
    });

};

function Login(){
    FB.login(function(response) {
        if (response.authResponse) {
            access= response.authResponse.accessToken;
            getUserInfo();
        } else {
            console.log('User cancelled login or did not fully authorize.');
        }
    },{scope: 'email,user_tagged_places'});
}

function getUserInfo() {
    FB.api('/me?fields=email,link,name', function(response) {
        console.log(response);
        var str="<b>Name</b> : "+response.name+"<br>";
        str +="<b>Username:</b> "+response.username+"<br>";
        str +="<b>id: </b>"+response.id+"<br>";
        str +="<b>Email:</b> "+response.email+"<br>";
        str +="<input type='button' value='Get Photo' onclick='getPhoto();'/>";
        str +="<input type='button' value='Get Check Ins' onclick='getCheckIns();'/>";
        str +="<input type='button' value='Logout' onclick='Logout();'/>";
        document.getElementById("status").innerHTML=str;
    });
}

function getPhoto(){
    FB.api('/me/picture?type=normal', function(response) {
        var str="<br/><b>Pic</b> : <img src='"+response.data.url+"'/>";
        document.getElementById("status").innerHTML+=str;
    });
}

function getCheckIns() {
    FB.api("/me?fields=tagged_places&access_token="+access, function(response) {
        console.log(response);
    });
}

function Logout(){
    FB.logout(function(){document.location.reload();});
}

// Load the SDK asynchronously
(function(d){
    var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement('script'); js.id = id; js.async = true;
    js.src = "//connect.facebook.net/en_US/all.js";
    ref.parentNode.insertBefore(js, ref);
}(document));