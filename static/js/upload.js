
var WildRydes = window.WildRydes || {};
WildRydes.map = WildRydes.map || {};
$(document).ready(function(){

function verifySignIn(){
    /*********
    *Makes sure the user is signed in first
    *redirects to signin.html if they are not
    *
    **********/
    WildRydes.authToken.then(function setAuthToken(token) {
        console.log(token);
        if (token) {
            authToken = token;
        } else {
            window.location.href = '/signin.html';
        }
    }).catch(function handleTokenError(error) {
        alert(error);
        window.location.href = '/signin.html';
    });
}


    function createPool(){
        var cognitoUserPool = {
            UserPoolId: _config.cognito.userPoolId,
            ClientId: _config.cognito.userPoolClientId
        };
        var userPool = new AmazonCognitoIdentity.CognitoUserPool(cognitoUserPool);
    var cognitoUser = userPool.getCurrentUser();

    //Constructing user pool identity provider sign
    //in string
    var userPoolSignIn = (
        'cognito-idp.'  + _config.cognito.region +
        + '.amazonaws.com/' +
        _config.cognito.userPoolId
    );
    if (cognitoUser != null) {
    	cognitoUser.getSession(function(err, result) {
    		if (result) {



    			console.log('Logged into user pool');


                AWS.config.region = _config.cognito.region;
    			// Add the User's Id Token to the
                // Cognito identity pool credentials config session
                AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    				IdentityPoolId: 'us-east-1:5b715989-3e44-4988-87ef-46a625c974b5'
                    //,
    				// Logins: {
    				// 	userPoolSignIn : result.getIdToken().getJwtToken()
    				// }
    			});

                console.log(AWS.config.credentials);

    		}
    	});
    }

}

function postS3Bucket(){
    // Create S3 service object
    s3 = new AWS.S3({apiVersion: '2006-03-01'});

    // Call S3 to list the buckets
    s3.listBuckets(function(err, data) {
      if (err) {
        console.log("Error", err);
      } else {
        console.log("Success", data.Buckets);
      }
    });
}

verifySignIn();
createPool();


});
