var firebaseConfig = {
    apiKey: "AIzaSyB5AqrECrbHCpj5rwRljxOdwnRk4mA2o70",
    authDomain: "congensys.firebaseapp.com",
    databaseURL: "https://congensys.firebaseio.com",
    projectId: "congensys",
    storageBucket: "congensys.appspot.com",
    messagingSenderId: "398327944447",
    appId: "1:398327944447:web:0e13b23c6e2c835f41e8ca"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  firebase.auth.Auth.Persistence.LOCAL;


  function login(email, password){

	firebase.auth().signInWithEmailAndPassword(email, password).then(function(){
		alert("logged in");
		var user = firebase.auth().currentUser;
		console.log(user);
		window.location = '/admin';
	}).catch(function(error) {
			var errorCode = error.code;
		  var errorMessage = error.message;
		  if (errorCode === 'auth/wrong-password') {
			  alert('Wrong password.');
		  } else {
			  alert(errorMessage);
		  }
		  console.log(error);
	  });
  }

  function logout(){
	firebase.auth().signOut().then(function() {
		  // Sign-out successful.
		  alert("Signed out");
		//   flag = false;
		  window.location.href = '/'
	}).catch(function(error) {
  	// An error happened.
	});
}

