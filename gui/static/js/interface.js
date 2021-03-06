/*
INTERFACE.

Pages and functions:
- getters
	- get ID
	- get IP
	- get power
- bot configs
	- addBot
	- removeBot
- bot dynamics
	- commandBot
	- ...
*/

//Anything left here is unimplemented in the new GUI, delete functions as they get implemented/converted
$("#ip").value = document.URL;
active_bots = [];
discovered_bots = [];

/* Getters */
function getIP(){
	return $("#ip").val();
}

function getPort(){
	return $("#port").val();
}

function getPower(){
	return $("#power").val();
}

/*
	For any update to the list of active bots, the dropdown menu
	of active bots will update accordingly (depending on the addition
	or removal of a bot).
*/
function updateDropdown(toAdd, text, val) {
	// if adding to update
	if(toAdd) { 
		var opt = document.createElement('option');
	    opt.text = text;
	    opt.value = val;
	    opt.className = "blist";
	    var botlist = document.getElementById("botlist");
		botlist.appendChild(opt);
	}

	// if removing to update
    else { 
    	var allBots = $("#botlist").getElementsByTagName("*");
    	var removed = false;
    	for(var i=0; i<allBots.length && !removed; i++) {
    		if(allBots[i].text === text) {
    			$("#botlist").removeChild(allBots[i]);
    			removed = true;
    		}
    	}
    }
}

function redoDropdown(data) {
    $('#botlist').empty();
    for (let i = 0; i < data.length; i++) {
		var opt = document.createElement('option');
	    opt.text = data[i].name;
	    opt.value = data[i].name;
	    opt.className = "blist";
	    var botlist = document.getElementById("botlist");
		botlist.appendChild(opt);
    }
}

/* Helper function called from the eventlistener
*/
function manageBots(option, name){
	$.ajax({
		method: "POST",
		url: getIP() + option,
		data: JSON.stringify({
			name: name
		}),
		processData: false,
		contentType: 'application/json'
	});
}

/*
    Get set of discoverable minibots
*/
function updateDiscoveredBots(){
    $.ajax({
        method: "POST",
        url: '/discoverBots',
        dataType: 'json',
        data: '',
        contentType: 'application/json',
        success: function (data) {
             //Check if discovered_bots and data are the same (check length and then contents)
            if(data.length != discovered_bots.length){
                //If not then clear list and re-make displayed elements
                redoDiscoverList(data);
            }
            else{
                //Check value to ensure both structures contain the same data
                for(let x=0;x<data.length;x++){
                    if(data[x]!=discovered_bots[x]){
                        redoDiscoverList(data);
                        //Prevent the list from being remade constantly
                        break;
                    }
                }
            }
            setTimeout(updateDiscoveredBots,3000); // Try again in 3 sec
        }
    });
}

/*
    Recreates the display of discovered minibots
*/
function redoDiscoverList(data){
    var discover_list = document.getElementById("discovered");

    //Clear all child elements from the display list
    $("#discovered").empty();
    discovered_bots = [];

    for (let i = 0; i < data.length; i++) {
        //Trim the forward-slash
        var ip_address = data[i].substring(1);

        if(!active_bots.includes(ip_address)){
            var bot_ip = document.createElement('p');
            var add_ip = document.createElement('button');
            var next = document.createElement('break');

            var display_text = document.createTextNode(ip_address);
            var button_text = document.createTextNode("add bot");
            add_ip.setAttribute("id", i); //Use i instead of IP addresses b/c not string friendly
            add_ip.value = ip_address;
            add_ip.className = "discoverbot";

            //Append site elements
            discover_list.appendChild(bot_ip);
            bot_ip.appendChild(display_text);
            bot_ip.appendChild(add_ip);
            bot_ip.appendChild(next);
            add_ip.appendChild(button_text);

            //Add minibot address to discovered list
            discovered_bots.push(ip_address);
        }
    }

    /*Listener created repeatedly here, because listener only bound to elements
    * that CURRENTLY have the class, doesn't account for future elements with that class
    */
    $('.discoverbot').click(function(event) {
        //Get minibot's IP address
        var target = $(event.target); //$target
        var button_id = target[0]
        var bot_ip = button_id.value;
        var bot_idx = button_id.id;

        //POST request to base station
        $.ajax({
            method: "POST",
            url: '/addBot',
            dataType: 'json',
            data: JSON.stringify({
                ip: bot_ip,
                port: 10000,
                name: bot_ip+"(discovered)",
                type: "minibot"
            }),
            contentType: 'application/json',
            success: function addSuccess(data) {
                console.log("Success!");
                updateDropdown(true, data, data);
            }
        });
        //Add to active_bots list
        active_bots.push(bot_ip);
        redoDiscoverList(discovered_bots);
    });
}