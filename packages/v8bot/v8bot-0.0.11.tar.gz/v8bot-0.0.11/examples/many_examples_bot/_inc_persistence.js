//-- this example demonstrate how to use the File object together with the JSON functions to nicely load and store data on the filesystem

//-- define the default values here
var bot_data = {
    "user2score": {}
};

function load_data() {
    if (!File.exists("example_bot.dat")) {
        write("example_bot.dat does not exists!\n");
        return;
    }
    write("loading example_bot.dat\n");
    try { //-- catch errors
        fp = File.open("example_bot.dat", "r");
        bot_data = JSON.parse(fp.read());
        fp.close();
    }
    catch(err) {
        write("error loading example_bot.dat\n");
    }
    finally {
        if (fp) fp.close(); //-- ensure the file gets closed
    }
}

function save_data() {
    try {
        fp = File.open("example_bot.dat", "w");
        fp.write(JSON.stringify(bot_data));
        fp.close();
    }
    catch(err) {}
    finally {
        if (fp) fp.close(); //-- ensure the file gets closed
    }
}

//-- load data on startup
load_data();

//-- save data every ten seconds
EventManager.add("EveryTenSeconds", [], save_data);

//-- save data at shutdown (this just works if the process terminates gracefully)
EventManager.add("Shutdown", [], save_data);
