//--
//-- register a new command !18 or !mature witch expects 1 argument
//-- turns on or off the 18+ flag for a channel
//-- needs admin/editor rights
//-- syntax: !mature <on|off>
//--
register_command(["18", "mature"], 1, function(command, channel, user, args) {
    //-- allow only for admins/editors (editors have role=admin)
    if (user.role != "admin")
        return;

    if (args[0] == "on") {
        write("setting channel '" + channel + "' media_mature flag to 'on'\n");     //-- write info to console
        result = ApiClient.update_livestream_nice(channel, {"media_mature": "1"});  //-- use the API to change the channel info
        if (result["livestream"][0]["media_mature"] == "1")                         //-- check the result
            send_chat_message(channel, "channel is now marked as 18+");             //-- send a confirmation chat message
    }
    else if (args[0] == "off") {
        write("setting channel '" + channel + "' media_mature flag to 'off'\n");
        result = ApiClient.update_livestream_nice(channel, {"media_mature": "0"});
        if (result["livestream"][0]["media_mature"] == "0")
            send_chat_message(channel, "channel is no longer marked as 18+");
    }
});
