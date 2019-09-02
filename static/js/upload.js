
var WildRydes = window.WildRydes || {};
WildRydes.map = WildRydes.map || {};


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
        'cognito-idp.'  + _config.cognito.region
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
    				IdentityPoolId: 'us-east-1:5b715989-3e44-4988-87ef-46a625c974b5',
                    RoleArn: 'arn:aws:iam::350255258796:role/Cognito_test_s3_identity_poolAuth_Role',
    				Logins: {
    					userPoolSignIn : result.getIdToken().getJwtToken()
    				}
    			});

                console.log(AWS.config.credentials.get());
                console.log("test message 1");
                console.log(AWS.config.credentials);
                AWS.config.credentials.get(function(){

                // Credentials will be available when this function is called.
                var accessKeyId = AWS.config.credentials.accessKeyId;
                var secretAccessKey = AWS.config.credentials.secretAccessKey;
                var sessionToken = AWS.config.credentials.sessionToken;
                console.log(accessKeyId);
            });

    		}
    	});
    }

}

function postS3Bucket(){
    console.log("s3 buckets");
    console.log(AWS.config.credentials);
    // Create S3 service object
    s3 = new AWS.S3({apiVersion: '2006-03-01'});

    var params = {
     Bucket: 'dev-sneakpeek-image-trailer-repo',
     Delimiter: '/',
     Prefix: ''
    }

    s3.listObjects(params, function (err, data) {
     if(err)throw err;
     console.log(data);
    });
}

verifySignIn();
createPool();
postS3Bucket();
