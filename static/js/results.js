
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



    function appendTable(){
        /*********
        *Appends html table with json response
        *
        **********/
        $.getJSON( "http://dev-sneakpeek.s3-website-us-east-1.amazonaws.com/js/test_results.json",
        function( json_response ) {
            console.log(json_response);
        //   var items = [];
        //   $.each( data.data, function( key, val ) {
        //     items.push( "<li id='" + key + "'>" + val + "</li>" );
        //   });
         /**
          $( "<ul/>", {
            "class": "my-new-list",
            html: items.join( "" )
          }).appendTo( "body" );
          */
        });

    }


    verifySignIn();



});
