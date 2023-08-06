//-- this demonstrates how to handle request to the built-in api server
//-- to use this, you have to start the bot using the ``--api-address <host:port>`` command line switch
//-- for the moment i do not recommend to make this server reachable from the internet
EventManager.add("ApiRequest", [], function(request) {
    write("ApiRequest: path=" + request.path + ", query=" + JSON.stringify(request.query) + "\n");

    if (request.path == "/channels") //-- /channels
        request.response(get_channels());
    else if (request.path == "/users") { //-- /users?c=channel
        write("get_channel_users=" + get_channel_users + "\n");
        request.response(get_channel_users(request.query["c"][0]));
    }
    else if (request.path == "/join") { //-- /join?c=channel1&c=channel2
        request.query["c"].forEach(function(c) { join_channel(c); });
        request.response(true);
    }
    else if (request.path == "/part") { //-- /part?c=channel1&c=channel2
        request.query["c"].forEach(function(c) { part_channel(c); });
        request.response(true);
    }
});
