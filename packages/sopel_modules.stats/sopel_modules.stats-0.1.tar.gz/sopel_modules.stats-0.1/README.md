# sopel-stats

Advanced stats tracking module for Sopel IRC bot.

#### Installation
```
Best way:  
pip install sopel_modules.stats  

Not so best way:  
git clone https://github.com/minsis/sopel-stats.git  
cd sopel-stats  
pip install .  
```

#### Commands
```
!words [nick] - Shows you word count of you or nick  
!gwords [nick] - Shows global word count of you or nick  
!stats [nick] - Shows you general stats of you or nick  
!gstats [nick] - Shows global stats of you or nick  
```

### TODO

* Separate helper functions into their own file
* Add a way to clear data via chat
* Add variables into dict for easier handling
* Add admin commands (e.g turn off count in room, user, etc)
