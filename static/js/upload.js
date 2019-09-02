$(document).ready(function(){

    //Clearing cache
    AWS.config.credentials.clearCachedId();
    function createPool(){
        var cognitoUserPool = {
            UserPoolId: _config.cognito.userPoolId,
            ClientId: _config.cognito.userPoolClientId
        };
        var userPool = new AmazonCognitoIdentity.CognitoUserPool(cognitoUserPool);
    var cognitoUser = userPool.getCurrentUser();

    if (cognitoUser != null) {
    	cognitoUser.getSession(function(err, result) {
    		if (result) {

                //Constructing user pool identity provider sign
                //in string
                var userPoolSignIn =  (
                    'cognito-idp.' + _config.cognito.region
                    + '.amazonaws.com/'
                    + _config.cognito.userPoolId
                );
    			console.log('You are now logged in.');

                console.log(result.getIdToken().getJwtToken());
    			// Add the User's Id Token to the
                // Cognito identity pool credentials config session
                AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    				IdentityPoolId: 'us-east-1:5b715989-3e44-4988-87ef-46a625c974b5',
    				Logins: {
    					userPoolSignIn : result.getIdToken().getJwtToken()
    				}
    			});
                AWS.config.region = _config.cognito.region;
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


createPool();
});
