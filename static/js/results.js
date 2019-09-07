
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






    verifySignIn();


});
