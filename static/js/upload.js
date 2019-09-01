
({
    function createPool(){
    var cognitoUserPool = {
        UserPoolId: _config.cognito.userPoolId,
        ClientId: _config.cognito.userPoolClientId
    };
    var userPool = new AmazonCognitoIdentity.CognitoUserPool(cognitoUserPool);
}
}(jQuery));
