#Guild Wars 2 World Boss Timer


##To Do
* Add different cmd colors. Red for active and yellow for upcoming
* Implement UI

##Input
####**_"timed_bosses.json"_** 
A file containing the timed bosses details and UTC spawn times in the following format:
    
    "Karka Queen" : {
        "category" : "Hardcore",
        "rank" : "Legendary",
        "waypoint" : "[&BNUGAAA=]",
        "wiki" : "http://wiki.guildwars2.com/wiki/Defeat_the_Karka_Queen_threatening_the_settlements",
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
