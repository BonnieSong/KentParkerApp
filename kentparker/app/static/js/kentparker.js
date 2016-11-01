function onGoogleSignIn(googleUser) {
	var profile = googleUser.getBasicProfile();
	console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
	console.log('Name: ' + profile.getName());
	console.log('Image URL: ' + profile.getImageUrl());
	console.log('Email: ' + profile.getEmail());
	$.get("/login_google/"+profile.getEmail())
}

function GoogleSignOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });
  }
  
function onFBSignIn(googleUser) {
	console.log('Try to connect to FB');
	var glb_uid = "";
	var glb_uname = "";
	FB.login(function (response) {
// 		console.log('Response1 ' + Object.keys(response) + '.');
// 		console.log('response.authResponse' + Object.keys(response.authResponse));
		// if (response.authResponse){
// 			console.log('Welcome!  Fetching your information.... ');
//        		FB.api('/me', function(response) {
//          		console.log('Good to see you, ' + response.email + '.');
//          		alert('Good to see you, ' + response.email + '.');
//        		});
//        }
        res = FB.getLoginStatus(function (response) {
//         	console.log('Response2 ' + Object.keys(response) + '.');
            if (response.status === 'connected') {  // Connected to Facebook
                var uid = response.authResponse.userID; // Get UID
                var accessToken = response.authResponse.accessToken; // Get accessToken
//                 console.log('authResponse ' + Object.keys(response.authResponse) + '.');
                $("#uid").html("UID：" + uid);
                FB.api('/me', function(response) {
	                glb_uid = response.id;
	                glb_uname = response.name;
					console.log('User Name is, ' + glb_uname + '.');
       				console.log('User Facebook ID is, ' + glb_uid + '.');
       				$.get("/login_facebook/"+glb_uid)
//     				console.log('Response3 ' + Object.keys(response) + '.');
     			});
                $("#accessToken").html("accessToken：" + accessToken);
            } else if (response.status === 'not_authorized') {  // Did not connected to Facebook
                alert("Please Authorize");
            } else {    // Did not signed in successfully
            }
            });
//             console.log('Response ' + Object.keys(response) + '.');
        }, { scope: "email" });
        
    // FB.api('/me', function(response) {
// 			console.log('User Name 2 is, ' + glb_uname + '.');
//        		console.log('User Facebook ID 2 is, ' + glb_uid + '.');
// //     		console.log('Response ' + Object.keys(response) + '.');
//      	});
//     console.log('res: ' + Object.keys(res));
//     alert("uid: " + glb_uid);
	// var profile = googleUser.getBasicProfile();
// 	console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
// 	console.log('Name: ' + profile.getName());
// 	console.log('Image URL: ' + profile.getImageUrl());
// 	console.log('Email: ' + profile.getEmail());
// 	$.get("/login_google/"+profile.getEmail())
}

function FBSignOut() {
// 	alert("logged out1");
    FB.logout();
    alert("Logged out");
    console.log('User signed out.');
  }