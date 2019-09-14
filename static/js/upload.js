/************************
*Handles image upload to S3
*
*Note: _config is set when the js/config.js
*script is run to populate build time variables
*For references dependent on cloudformation resource
*creation
*
*************************/
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
        				IdentityPoolId: _config.cognito.IdentityPoolId,
                        RoleArn: _config.cognito.IdentityAuthorizedRoleArn,
        				Logins: {
        					[userPoolSignIn] : result.getIdToken().getJwtToken()
        				}
        			});


                    AWS.config.credentials.get(function(){

                    // Credentials will be available when this function is called.
                    var accessKeyId = AWS.config.credentials.accessKeyId;
                    var secretAccessKey = AWS.config.credentials.secretAccessKey;
                    var sessionToken = AWS.config.credentials.sessionToken;
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
         Bucket: _config.backend.ImageUploadBucket,
         Delimiter: '/',
         Prefix: ''
        }

        s3.listObjects(params, function (err, data) {
         if(err)throw err;
         console.log(data);
        });
    }

    function addPhoto(bucketName) {
    console.log("Function Fired")
      var files = document.getElementById('photo-upload').files;
      if (!files.length) {
        return alert('Please choose a file to upload first.');
      }
      s3 = new AWS.S3({
          apiVersion: '2006-03-01',
          params:{Bucket: bucketName}}
        );
      var file = files[0];
      var fileName = file.name;
      //url encodes the bucket name
      var imagePhotoKey = encodeURIComponent(bucketName) + '//';
      console.log(AWS.config);

      var photoKey = imagePhotoKey + fileName;

      var params = {
        ACL: 'public-read',
        Bucket:bucketName,
        Key: fileName,
        Body: file,
        ContentType: file.type
    };
    /*
        Uploads image to s3 bucket
    */
      s3.upload(params, function(err, data) {
        if (err) {
            console.log(err);
          return alert('There was an error uploading your photo: ', err.message);
        }else {
                    console.log(data);
                }
        alert('Successfully uploaded photo.');

      });
    }

    
    verifySignIn();
    createPool();
    postS3Bucket();

    var input_file = document.getElementById('photo-upload');
    input_file.addEventListener('change', function() {
       //ajax call using _config bucket name
       addPhoto(_config.backend.ImageUploadBucket);

   });

    /* Old uploader
    var button = document.getElementById('upload-button');
    button.addEventListener('click', function() {
       //ajax call using _config bucket name
       addPhoto(_config.backend.ImageUploadBucket);

   });
   */

});
