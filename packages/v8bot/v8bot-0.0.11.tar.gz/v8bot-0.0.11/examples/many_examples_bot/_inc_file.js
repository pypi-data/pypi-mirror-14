//--
//-- demonstration how to use the File object
//--

function log(text) {
    //-- open example_bot.log for appending (a)
    //-- path traversal attacks are prevented, the user can't escape the working directory
    fp = File.open("..\\example_bot.log", "a");
    fp.write(text + "\n");
    fp.close();
}

EventManager.add("ChatMessage", [], function(timestamp, channel, user, content) {
    if (content.is_buffer) return; //-- skip chat log
    if (content.is_media) return; //-- skip images etc.

    //-- write chat log
    log("[" + channel + "] <" + user.name + "> " + content.text);
});
