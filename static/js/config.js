

/**********************
*This ensures that the getJSON is a synchronous
*call, makes sure that nothing else is done
*until the json is loaded
************************/
$.ajaxSetup({
    async: false
});

/********************************
*Loads the json file and assigns it
*to the _config variable of window object
*That way anytime config.js is loaded
*the cognito user pool information in addition to
*the api url will be available
*********************************/
$.getJSON("js/cognito_config.json",
    function(json_config) {
        window._config = json_config;

});
