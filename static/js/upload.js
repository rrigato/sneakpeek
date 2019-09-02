
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


        if (cognitoUser != null) {
        	cognitoUser.getSession(function(err, result) {
        		if (result) {

                    //Constructing user pool identity provider sign
                    //in string
                    var userPoolSignIn = (
                        'cognito-idp.'  + _config.cognito.region
                     + '.amazonaws.com/' +
                        _config.cognito.userPoolId
                    );

                    console.log(userPoolSignIn);
        			console.log('Logged into user pool');


                    AWS.config.region = _config.cognito.region;
        			// Add the User's Id Token to the
                    // Cognito identity pool credentials config session
                    //[] allows you to use a variable as an object key
                    AWS.config.credentials = new AWS.CognitoIdentityCredentials({
        				IdentityPoolId: 'us-east-1:5b715989-3e44-4988-87ef-46a625c974b5',
                        RoleArn: 'arn:aws:iam::350255258796:role/Cognito_test_s3_identity_poolAuth_Role',
        				Logins: {
        					[userPoolSignIn] : result.getIdToken().getJwtToken()
        				}
        			});

                    console.log("test message 1");

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

    function addPhoto(albumName) {
      var files = document.getElementById('photo-upload').files;
      if (!files.length) {
        return alert('Please choose a file to upload first.');
      }
      var file = files[0];
      var fileName = file.name;
      var albumPhotosKey = encodeURIComponent(albumName) + '//';

      var photoKey = albumPhotosKey + fileName;
      s3.upload({
        Key: photoKey,
        Body: file,
        ACL: 'public-read'
      }, function(err, data) {
        if (err) {
          return alert('There was an error uploading your photo: ', err.message);
        }
        alert('Successfully uploaded photo.');

      });
    }

    verifySignIn();
    createPool();
    postS3Bucket();


});
