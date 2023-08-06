//--------------------------------------------------------------------------------------------------------------------------------
//-- configuration
//--------------------------------------------------------------------------------------------------------------------------------

var HOSTER_CHANNEL = "uranoxyd";        //-- name of the owners channel

var MIN_HOSTING_DURATION = 60 * 10;     //-- minimun hosting duration
var MAX_HOSTING_DURATION = 60 * 60;     //-- maximun hosting duration

//--------------------------------------------------------------------------------------------------------------------------------
//-- main script dont change anything if you dont know what you do
//--------------------------------------------------------------------------------------------------------------------------------

var FOLLOWERS = [];                     //-- list of all followers
var FOLLOWERS_LIVE = [];                //-- list of followers that are live

var CURRENTLY_HOSTING = null;           //-- channel that is currently hosted or null if none
var LAST_HOSTED = null;                 //-- channel that was hosted last time
var HOSTING_SINCE = 0;                  //-- timestamp the current hosting started at
var CURRENT_HOSTING_DURATION = 0;       //-- time in seconds the current channel is hosted

function choice(inp) {
    //-- pick a random element from a array
    return inp[ Math.floor(Math.random() * inp.length) ];
}

function channel_is_live(channel) {
    //-- returns true if ``channel`` is live
    return ApiClient.get_channel_status(channel)["media_is_live"] != "0";
}

function set_host_mode(hoster_channel, hosted_channel) {
    //-- sets the host mode property for a channel
    ApiClient.update_livestream_nice(hoster_channel, {"media_hosted_name": hosted_channel})
}

function fetch_followers() {
    //-- fetch list of followers and build a list with their usernames
    var followers = [];
    ApiClient.get_channel_followers(HOSTER_CHANNEL).forEach(function(e) {
        followers.push(e.user_name);
    });

    FOLLOWERS = followers;
    Log.debug("followers: %s", JSON.stringify(followers));
}

function update_live_followers() {
    //-- build a list with the usernames of all live followers
    var followers_live = [];
    FOLLOWERS.forEach(function(f) {
        if (channel_is_live(f))
            followers_live.push(f);
    });

    FOLLOWERS_LIVE = followers_live;

    if (followers_live.length > 0)
        Log.debug("live followers: %s", JSON.stringify(followers_live));
}

function startup() {
    fetch_followers();
    update();
}

function update() {
    //--
    //-- gets called every minute and is the main function for the script
    //--

    //-- if the hoster channel is live, dont do anything
    if (channel_is_live(HOSTER_CHANNEL))
        return;

    //-- test which followers are live
    update_live_followers();

    //-- end hosting if hosted user gets offline
    if (CURRENTLY_HOSTING != null && FOLLOWERS_LIVE.indexOf(CURRENTLY_HOSTING) == -1) {
        Log.info("currently hosted channel '%s' is now offline, ending host mode", CURRENTLY_HOSTING);
        set_host_mode(HOSTER_CHANNEL, "off");
        CURRENTLY_HOSTING = null;
    }

    //-- no followers are live
    if (FOLLOWERS_LIVE.length == 0)
        return;

    //-- calculate the hosting duration for a channel, if more then one channel is live
    //-- MAX_HOSTING_DURATION gets divided by the count of live channels
    var calculated_hostig_duration = MAX_HOSTING_DURATION;
    if (FOLLOWERS_LIVE.length > 1) {
        calculated_hostig_duration = Math.min(
            Math.floor(MAX_HOSTING_DURATION / FOLLOWERS_LIVE.length),
            MIN_HOSTING_DURATION
        );
    }

    //-- write a info message about the currently hosted channel and duration
    if (CURRENTLY_HOSTING != null) {
        CURRENT_HOSTING_DURATION = time() - HOSTING_SINCE;
        Log.info("hosting '%s' since %i sec. ends in %i sec.", CURRENTLY_HOSTING, CURRENT_HOSTING_DURATION, calculated_hostig_duration-CURRENT_HOSTING_DURATION);
    }

    //-- pick a channel to host
    if (CURRENTLY_HOSTING == null || CURRENT_HOSTING_DURATION >= calculated_hostig_duration) {
        Log.debug("picking user to host ...");

        var picked_channel = null;
        if (FOLLOWERS_LIVE.length > 1) {
            //-- avoid hosting the same channel twice if more the 1 candidates are live
            while (true) {
                picked_channel = choice(FOLLOWERS_LIVE);
                if (picked_channel != LAST_HOSTED)
                    break;
                }
        }
        else {
            picked_channel = choice(FOLLOWERS_LIVE);
        }

        Log.debug("picked '%s' as new channel", picked_channel);
        HOSTING_SINCE = time();
        LAST_HOSTED = CURRENTLY_HOSTING;

        if (CURRENTLY_HOSTING != picked_channel) {
            CURRENTLY_HOSTING = picked_channel;
            Log.debug("starting to host channel '%s'", picked_channel);
            Log.info("now hosting '%s' for %.01f minutes.", picked_channel, calculated_hostig_duration/60);

            set_host_mode(HOSTER_CHANNEL, picked_channel);
        }
    }
}

EventManager.add("Startup", [], startup);
EventManager.add("EveryMinute", [], update);
EventManager.add("EveryFifteenMinutes", [], fetch_followers);
