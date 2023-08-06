//-- helper function
function request_commercial(channel, count) {
    write("request " + count + " commercial(s) for channel '" + channel +"'\n");
    ApiClient.commercial_break(channel, count);
}

//-- command !ad or !commercial [count]
register_command(["ad", "commercial"], 1, function(command, channel, user, args) {
    //-- allow only for admins/editors (editors have role=admin)
    if (user.role != "admin")
        return;

    count = 1;
    if (args.length > 0) {
        count = parseInt(args[0]);
        if (isNaN(count))
            count = 1;
    }

    request_commercial(channel, count);
});

//-- try do a commercial break every 30 minutes in all channels
EventManager.add("EveryThirtyMinutes", [], function() {
    get_channels().forEach(function (c) {
        request_commercial(c, 1);
    });
});
