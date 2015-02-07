#Guild Wars 2 World Boss Timer
------------


##Input
####**_"timed_bosses.json"_** 
A file containing the timed bosses details and UTC spawn times in the following format:
    
    "Karka Queen" : {
        "category" : "Hardcore",
        "rank" : "Legendary",
        "location" : "Southsun Cove",
        "waypoint" : {
            "name" : "Pearl Islet",
            "link" : "[&BNUGAAA=]"},
        "wiki" : "http://wiki.guildwars2.com/wiki/Defeat_the_Karka_Queen_threatening_the_settlements",
        "average_time" : "120",
        "times" : ["02:00", "06:00", "10:30", "15:00", "18:00", "23:00"],
        "loot" : [
            {"Dragonite Ore" : "30"},
            {"Rare or Exotic Items" : "2"},
            {"Champion Loot Bags" : "2"}]
    }

##Output
* Time till next boss
* Encounter/Total Encounters (Derived from the position of the current time in the total set of that bosses times)
* Special loot available?


#TODO
* Sort the active times
* Set the focus of the window to the main panel when it open so that scrolling works straight away
* Finish the menu items