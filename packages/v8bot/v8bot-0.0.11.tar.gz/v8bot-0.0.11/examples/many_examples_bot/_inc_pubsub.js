//-- this demonstrates how to use the built-in "pubsub" server, it is a normal HTTP-Server wich uses a simple "Long Polling" technic
//-- to use this, you have to start the bot using the ``--pubsub-address <host:port>`` command line switch
//-- for the moment i do not recommend to make this server reachable from the internet
//-- to make the pubsub_client/index.html work, the server should listen on localhost:4242 or you have to change the ``poll_url`` field in the index.html
EventManager.add("ChatMessage", [], function(timestamp, channel, user, content) {
    if (content.is_buffer) return; //-- skip chat log
    if (content.is_media) return; //-- skip images etc.

    //-- publish the message on the channel 'main'
    publish_message("main", {"channel": channel, "user": user, "content": content});
});
