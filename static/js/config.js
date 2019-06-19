//<script type="text/javascript" src="js/cognito_config.json"></script>
/***************
Loads a json from the cognito_config.json file
and assigns that json to the window._config variable
*****************

var x = $.getJSON("/js/cognito_config.json",
    function(json_config) {
        return(json_config);

});



window._config = {
    cognito: {
        userPoolId: 'us-east-1_uWSFSS2Ph', // e.g. us-east-2_uXboG5pAb
        userPoolClientId: '16vk70001evfl5bhs21g6knf63', // e.g. 25ddkmj4v6hfsfvruhpfi7n4hv
        region: 'us-east-1' // e.g. us-east-2
    },
    api: {
        invokeUrl: '' // e.g. https://rc7nyt4tql.execute-api.us-west-2.amazonaws.com/prod',
    }
};
*/


$.ajaxSetup({
    async: false
});


$.getJSON("js/cognito_config.json",
    function(json_config) {
        console.log(json_config);
        window._config = json_config;

});


console.log("hello world 2");
