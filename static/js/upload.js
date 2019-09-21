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

    /**
     *Makes sure the user is signed in first
     *redirects to signin.html if they are not
     * s3
     * @param {}
     * @returns {html} signin.html or upload.html
     */
    function verifySignIn(){
        /*********
        *Redirects to signin.html if
        * the user is not signed in
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

/**
 * Connects to cognito user pool and
 * uses that authentication in order to
 * authorize with aws identity pool to access
 * s3
 * @param {}
 * @returns {credentials} AWS.config.credentials
 *object which gets sts short term tokens
 */
function createPool(){


    var cognitoUserPool = {
        UserPoolId: _config.cognito.userPoolId,
        ClientId: _config.cognito.userPoolClientId
    };
    var userPool = new AmazonCognitoIdentity.CognitoUserPool(
        cognitoUserPool);
    var cognitoUser = userPool.getCurrentUser();


    if (cognitoUser != null) {


    	cognitoUser.getSession(function(err, result) {
            /*************************
            *Establishes cognito user pool session
            *and gets aws credentials to use for
            *gets cognito identity pool sts role
            ***************************/
    		if (result) {

                    //Constructing user pool identity provider sign
                    //in string
                    var userPoolSignIn = (
                        'cognito-idp.'  + _config.cognito.region
                     + '.amazonaws.com/' +
                        _config.cognito.userPoolId
                    );



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

    /**
    *Prepares the file uploaded by the
    *user to make an s3 put operation using
    *the javascript sdk
     * @param {bucketName} string Name of the bucket
     * for the upload
     * @param {loadNumber} int Numeric Load identifier
     * for the trailer
     * @param {trackingNumber} string Tracking number
     * for the trailer
     * @returns {result_message} Either prompts for
     * an error or displays a sucess message
     */
    function addPhoto(bucketName, loadNumber = -1,
        trackingNumber='testNumber') {
      var files = document.getElementById('photo-upload').files;
      if (!files.length) {
        return alert('Please choose a file to upload first.');
      }
      /*
      *AWS SDK for s3 is setup with the
      *credentials that are retrieved by createPool
      */
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
      //parameters for s3 upload
      //Tagging must be key=Value
      var load_id = 'loadid=' + loadNumber;
      var params = {
        ACL: 'private',
        Bucket:bucketName,
        Key: fileName,
        Body: file,
        ContentType: file.type,
        Tagging: load_id
    };
    /*
        Uploads image to s3 bucket
    */
      s3.upload(params, function(err, data) {
        if (err) {
            console.log(err);
          return alert('There was an error uploading your photo: ', err.message);
        }else {
                    displaySuccess();
                }

      });
    }


    /**
     * Displays sucessful uplaod information
     * as applicable
     * @param {display_message} string message you
     *want the div to display after upload
     * @returns {}
     */
    function displaySuccess(
        display_message="You Have uploaded an image"){
        var success_div = document.getElementById(
            "success-message");


        //Makes div visibilbe then changes
        //message inside of div
        success_div.style.display = "block";

        success_div.innerText= display_message;
    }


    /**
     * Hides the uploader once we have a successful
     *image and unhides a button that returns to the
     * upload homepage
     * @param {}
     * @returns {}
     */
    function addReturnButton(){
        var retry_upload_div = document.getElementById(
            "try-again");
        var hide_file_upload = document.getElementById(
            "file-uploader-wrapper");

        //Makes div return button visibile and hides
        //the uploader div
        retry_upload_div.style.display = "block";

        hide_file_upload.style.display = "none";

    }

    /**
     * Displays an image preview before the upload
     *
     * @param {input} this passes the global object
     * @returns {thumbnail-preview} div Contains
     *the image as a background thumbnail
     *
     *inspiration for image preview comes from
     *this codepen
     *https://codepen.io/siremilomir/pen/jBbQGo
     */
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#imagePreview').css('background-image', 'url('+e.target.result +')');

            }
            reader.readAsDataURL(input.files[0]);
            var image_preview = document.getElementsByClassName(
                "thumbnail-preview");

            //Makes div visibilbe with the
            //with the image upload preview
            image_preview[0].style.display = "block";
        }
        addReturnButton();
    }



    verifySignIn();
    createPool();

    var input_file = document.getElementById('photo-upload');
    input_file.addEventListener('change', function() {
       //ajax call using _config bucket name
       readURL(this);
       addPhoto(_config.backend.ImageUploadBucket);

   });



   /**
   *overlay logic: inspired from this codepen:
   *https://codepen.io/rkpasia/pen/LNEQod
   *records the load id value
   */
   $('.email').on("change keyup paste",
     function(){
       if($(this).val()){

         $('.icon-paper-plane').addClass("next");
       } else {
         $('.icon-paper-plane').removeClass("next");
       }
     }
   );

   $('.next-button').hover(
     function(){
       $(this).css('cursor', 'pointer');
     }
   );

   $('.next-button.email').click(
     function(){

        console.log($(this).val());
       $('.email-section').addClass("fold-up");
       $('.password-section').removeClass("folded");
     }
   );




});
