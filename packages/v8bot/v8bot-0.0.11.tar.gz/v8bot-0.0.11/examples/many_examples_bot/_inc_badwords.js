var score_to_timeout = 20;				//-- score at wich the user gets a timeout
var timeout_time = 60;					//-- timeout duration
var score_reduction_per_sec = 0.1;		//-- score "cooldown"

//-- define regular expression with bad words and give them a score
var bad_patterns = [
    [/heil hitler/i, 100],
    [/hurensohn/i,    10],
];

register_command("score", 0, function(command, channel, user, args) {
    var user_score = bot_data.user2score[user.name];
    send_direct_message(channel, user.name, "your current badword score is " + (Math.round(user_score * 10) / 10));
});

EventManager.add("ChatMessage", [], function (timestamp, channel, user, content) {
    if (content.is_buffer) return; //-- ignore chat log
    if (content.is_media) return; //-- ignore images etc.

    //-- iterate over all bad_pattern entries
    bad_patterns.forEach(function(entry) {
        match = entry[0].test(content.text);
        if (match > 0) { //-- test if pattern matched
            score = entry[1];

            if (user.name in bot_data.user2score) {
                bot_data.user2score[user.name] += score;
            }
            else {
                bot_data.user2score[user.name] = score;
            }
            var user_score = bot_data.user2score[user.name];

            //-- inform user about the score change
            send_direct_message(channel, user.name, user.name + " your badword score is now " + (Math.round(user_score * 10) / 10) + "!");

            //-- test if the score for the user reached the limit and timeout him if so
            if (user_score >= score_to_timeout) {
                write("kicking user '" + user.name + "' from channel '" + channel + "' timeout=" + timeout_time + "\n");
                kick_user(channel, user.name, timeout_time);
            }
        }
    });
});

EventManager.add("EverySecond", [], function() {
    //-- every second reduce the score for all users by score_reduction_per_sec
    for (var user in bot_data.user2score) {
        bot_data.user2score[user] = Math.max(bot_data.user2score[user] - score_reduction_per_sec, 0);
    };
});
