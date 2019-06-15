/***************
Loads a json from the cognito_config.json file
and assigns that json to the window._config variable 
*****************/
$.getJSON("test.json",
    function("cognito_config.json") {
        window._config = json
});
