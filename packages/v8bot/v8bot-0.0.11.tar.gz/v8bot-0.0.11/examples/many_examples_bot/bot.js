var version = "1.0";

include("examples\\many_examples_bot\\_inc_persistence.js");
include("examples\\many_examples_bot\\_inc_file.js");
include("examples\\many_examples_bot\\_inc_ads.js");
include("examples\\many_examples_bot\\_inc_badwords.js");
include("examples\\many_examples_bot\\_inc_mature.js");
include("examples\\many_examples_bot\\_inc_api.js");
include("examples\\many_examples_bot\\_inc_pubsub.js");

//-- simple command !say returns the text to the user
register_command("say", 0, function(command, channel, user, args) {
    send_chat_message(channel, "you say " + args + " i say " + args + "!");
});

//-- another very simple command !version, outputs the bot version and the v8bot version string to the chat
register_command("version", 0, function(command, channel, user, args) {
    send_chat_message(channel, "example bot v" + version + " running on " + __version__);
});

//-- simple command !say returns the text to the user
register_command("part", 1, function(command, channel, user, args) {
    if (!user.is_owner) return;
    part_channel(args[0]);
});

//-- demonstrate how to handle the 'ChatMessage' event
EventManager.add("ChatMessage", [], function(timestamp, channel, user, content) {
    if (content.is_buffer) return; //-- skip chat log
    if (content.is_media) return; //-- skip images etc.

    write("[" + channel + "] <" + user.name + "> " + content.text);
});

//-- some example events
EventManager.add("Startup", [], function() {
    write("startup\n");
});

EventManager.add("ChannelJoined", [], function(channel, name, role) {
    write("joined channel '" + channel + "' as '" + name + "' with role=" + role + "\n");
});

EventManager.add("ChannelParted", [], function(channel) {
    write("left channel '" + channel + "\n");
});
