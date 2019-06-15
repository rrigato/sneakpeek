//<script type="text/javascript" src="js/cognito_config.json"></script>
/***************
Loads a json from the cognito_config.json file
and assigns that json to the window._config variable
*****************/

$.getJSON(window.location.hostname + "/js/cognito_config.json",
    function(json_config) {
        window._config = json_config
});

console.log("hello world 2");
