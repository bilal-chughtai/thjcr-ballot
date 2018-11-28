var currentlySelected = "bbc_a";

//the following object translates between the site button's ID and that site's URI

//map of sites (split up by plan)
var sites  = {
	"bbc_a" : {
		sitePlanRes : 'bbc-a-floor-combined.svg',	//for loading plan 
		roomData : [],
		sitePrefixes : [{'prefix':"bbc_a", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"bbc_b" : {
		sitePlanRes : 'bbc-b-floor-combined.svg',
		roomData : [],
		sitePrefixes : [{'prefix':"bbc_b", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"bbc_c" : {
		sitePlanRes : 'bbc-c-floor-combined.svg',
		roomData : [],
		sitePrefixes : [{'prefix':"bbc_c", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"cs_1" : {
		sitePlanRes : 'cs-first-floor-combined.svg',
		etag : -1, //for caching
		roomData : [],
		sitePrefixes : [{'prefix':"cs_1", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"cs_2" : {
		sitePlanRes : 'cs-second-floor-combined.svg',
		etag : -1, //for caching
		roomData : [],
		sitePrefixes : [{'prefix':"cs_2", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"boho_a" : {
		sitePlanRes : 'boho-a-floor-combined.svg',	
		etag : -1, //for caching
		roomData : [],
		sitePrefixes : [{'prefix':"boho_a", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"boho_b" : {
		sitePlanRes : 'boho-b-floor-combined.svg',
		etag : -1, //for caching
		roomData : [],
		sitePrefixes : [{'prefix':"boho_b", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"boho_c" : {
		sitePlanRes : 'boho-c-floor-combined.svg', 		
		etag : -1, //for caching
		roomData : [],
		sitePrefixes : [{'prefix':"boho_c", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"new_build-a" : {
		sitePlanRes : 'new-build-a-stair_combined.svg',		
		etag : -1, //for caching
		roomData : [],
		sitePrefixes : [{'prefix':"new_build_a", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"new_build_e-f-g-h-i-j" : {
		sitePlanRes : 'new-build-e-f-g-h-i-j-stair_combined.svg',
		etag : -1, //for caching
		roomData : [],
		sitePrefixes : [{'prefix':"new_build_e", 'etag':-1},{'prefix':"new_build_f", 'etag':-1},{'prefix':"new_build_g", 'etag':-1},{'prefix':"new_build_h", 'etag':-1},{'prefix':"new_build_i", 'etag':-1},{'prefix':"new_build_j", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"new_build_k-l-m-n-o-p" : {
		sitePlanRes : 'new-build-k-l-m-n-o-p-stair_combined.svg',
		etag : -1, //for caching
		roomData : [],
		sitePrefixes : [{'prefix':"new_build_k", 'etag':-1},{'prefix':"new_build_l", 'etag':-1},{'prefix':"new_build_m", 'etag':-1},{'prefix':"new_build_n", 'etag':-1},{'prefix':"new_build_o", 'etag':-1},{'prefix':"new_build_p", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"wyng_a" : {
		sitePlanRes : 'wyng-a-floor-combined.svg',	
		etag : -1, //for caching
		roomData : [],
		sitePrefixes : [{'prefix':"wyng_a", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	}, 
	"wyng_b" : {
		sitePlanRes : 'wyng-b-floor-combined.svg',
		etag : -1, //for caching
		roomData : [],
		sitePrefixes : [{'prefix':"wyng_b", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"wyng_c" : {
		sitePlanRes : 'wyng-c-floor-combined.svg',
		etag : -1, //for caching
		roomData : [],
		sitePrefixes : [{'prefix':"wyng_c", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	}, 
	"wyng_d" : {
		sitePlanRes : 'wyng-d-floor-combined.svg',
		etag : -1, //for caching
		roomData : [],
		sitePrefixes : [{'prefix':"wyng_d", 'etag':-1}] //list of room ID prefixes in this site, corresponding to one remote .json
	},
	"coote" : {
		sitePlanRes : 'coote-house.svg',
		roomData : [],
		sitePrefixes : [{'prefix':"coote", 'etag':-1}]
	}
}


function loaded() {
	var im = document.getElementById("svg_image");
	var container = document.getElementById("svg_container");
	im.width = container.clientWidth;
	loadSVG(document.getElementById(currentlySelected));
	updateAll();
	recurInterval = setInterval(updateAll, 50000);	
}

function updateAll() {

    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 200) {
            data = JSON.parse(request.response);
            updatedData(data)
        }
    }
        
    httpRequest.open("GET", "data/data.json", true);
    httpRequest.send();
}

function updateSite(site) {
	for (var i = 0; i < sites[site].sitePrefixes.length; i++) {
		var sitePrefix = sites[site].sitePrefixes[i].prefix; //make a copy not a reference?
		var httpRequest = new XMLHttpRequest();
		httpRequest.onreadystatechange = function(request, site, prefixIndex) {
			return function() {
				var priorEtag = sites[site].sitePrefixes[prefixIndex].etag;
				if (request.readyState == 4 && request.status == 200){ // && priorEtag != request.getResponseHeader("etag")) {
					updatedData(site, JSON.parse(request.response));
					sites[site].sitePrefixes[prefixIndex].etag = request.getResponseHeader("etag");
				}
			}
		} (httpRequest, site, i);
		httpRequest.open("GET", "data/" + sitePrefix + ".json", true);
		console.log("getting: data/" + sitePrefix +".json");
		httpRequest.send();
	}
}

// this gets called when we know the data has changed
function updatedData(data) {
    for (let site in data) {
        site_data = data[site];
        let roomsUpdated = updateAndGetDifferencesFor(site, roomsJSON);
	console.log("Rooms updated for site: " +site);
	console.log(roomsUpdated);
	if (Object.keys(roomsUpdated).length > 0) {
		notify(roomsUpdated);
		if (currentlySelected == site) {
			updateSvgData(currentlySelected);
		} else {
			//var notifier = document.getElementById(site).getElementsByClassName("indicator")[0];
			//notifier.style.backgroundColor = "blue";
			//notifier.parentElement.title = "has changes";
		}
	}
    }
}


//for notification panel
function notify(roomDifferences) {
	var oldstatus = "";
	var newstatus = ""; //No idea if this help reduce number of variable allocations in javascript... probably optimizied away
	var updatesPane = document.getElementById("updates_pane");

	for (var room in roomDifferences) {
		newstatus = roomDifferences[room].status;
		if (newstatus == "occupied") {
			var div = document.createElement("div")
			div.setAttribute("class", "updates_row updates_taken");
			div.innerHTML = roomDifferences[room].occupier  + " has taken " + roomDifferences[room].roomName;
			updatesPane.insertBefore(div, updatesPane.firstChild);	
		} else if (newstatus == "available") {
			var div = document.createElement("div")
			div.setAttribute("class", "updates_row updates_freed");
			div.innerHTML = roomDifferences[room].roomName + " has become available";
			updatesPane.insertBefore(div, updatesPane.firstChild);	
		} else {
			//do nothing because it's some odd case
		}
	}
}


function updateAndGetDifferencesFor(site, newRoomsJSON) {
	var changedRooms = {};
	//console.log(newRoomsJSON);
	for (var r in newRoomsJSON) {
		//console.log(r);
		if (!sites[site].roomData[r] || newRoomsJSON[r].occupier != sites[site].roomData[r].occupier) {
			sites[site].roomData[r] = newRoomsJSON[r];
			changedRooms[r] = newRoomsJSON[r];
		}
	}
	return changedRooms;
}


//only operates on the currently loaded svg
function updateSvgData(s) {
	var site = sites[s];
	var svg = document.getElementById("svg_image").contentDocument;
	for (var room in site.roomData) {
		//console.log("Room being processed: " + room);
		var r = svg.getElementById(room);
		if (!r) {
			console.log("COULD NOT FIND IN SVG: " + room);
			continue;
		}
		var roomStatus = site.roomData[room].status;
		//console.log("\tRoom status: " + roomStatus);
		if (roomStatus == "unavailable") {
			//console.log("\t\t unavailable");
			r.setAttribute("style","");
			r.setAttribute("class", "unavailable");
		} else if ( roomStatus == "available") {
			//console.log("\t\t available");
			r.setAttribute("class", "available");
		} else if (roomStatus == "occupied") {
			//console.log("\t\t occupied");
			r.setAttribute("class", "occupied");
		}
		r.setAttribute("style", "");
		r.setAttribute('onmouseout', 'top.hideTooltip()');
		r.setAttribute('onmouseover', 'top.showTooltip(evt,"'+s+'","' +room+'")');
	}	
}

function showTooltip(elem, site, room) {
	console.log("SHOWING TOOLTIP");
	var roomData = sites[site].roomData[room];
	var im = document.getElementById("svg_image");
	//calculate the offsets of the image initially
	var sidebar = document.getElementById("sidebar");
	var sidebarWidth = sidebar.getBoundingClientRect().width;
	var header = document.getElementById("header_container");
	var headerHeight = header.getBoundingClientRect().height;
	var imLeft = im.getBoundingClientRect().left;
	var imTop = im.getBoundingClientRect().top;
	document.getElementById("room").innerHTML = roomData.roomName;
	document.getElementById("occupant").innerHTML = roomData.occupier;
	if (roomData.occupierCrsid.trim().length > 0) {
		document.getElementById("crsid").innerHTML = "("+roomData.occupierCrsid+")";
	} else {
		document.getElementById("crsid").innerHTML = ""
	}

		
	document.getElementById("contract_type").innerHTML = roomData.contractType;
	document.getElementById("rent").innerHTML = "&pound;"+roomData.roomPrice;
	document.getElementById("room_type").innerHTML = roomData.roomType;
	document.getElementById("floor").innerHTML = roomData.floor;
	document.getElementById("notes").innerHTML = roomData.notes;
	if (roomData.fullCost.indexOf("\n") != -1) {
		var s = roomData.fullCost.split("\n");
		document.getElementById("total_cost_1").innerHTML = s[0];
		document.getElementById("total_cost_2").innerHTML = s[1];
	} else {
		document.getElementById("total_cost_1").innerHTML = roomData.fullCost;
		document.getElementById("total_cost_2").innerHTML="";
		document.getElementById("total_cost_3").innerHTML="";
	}
	var tooltip = document.getElementById("tooltip");
	var elemPos = elem.target.getBoundingClientRect(); //this is constant depending on zoom level
	var posLeft = (imLeft + elemPos.left - sidebarWidth + elemPos.width/2 - tooltip.getBoundingClientRect().width/2) + "px";
	var posTop = Math.max(-headerHeight,(imTop + elemPos.top - headerHeight - tooltip.getBoundingClientRect().height - 10)) + "px";
	tooltip.style.left = posLeft;
	tooltip.style.top = posTop;
	tooltip.style.visibility = "visible";
	console.log(tooltip);
	tooltip.zIndex = "5";
}

function hideTooltip() {
	var tooltip = document.getElementById("tooltip");
	tooltip.style.visibility = "hidden";
	tooltip.zIndex = "-5";
}

function zoomIn() {
	var im = document.getElementById("svg_image");
	//im.height = im.height * 1.1;
	im.width = im.width * 1.1;
}

function zoomOut() {
	var im = document.getElementById("svg_image");
	//im.height = im.height * 0.9;
	im.width = im.width * 0.9;
}

var orig_width;
function zoomReset() {
	var im = document.getElementById("svg_image");
	im.width = orig_width;
}

//from parameters is DOM node that is clicked on
//parent ID is site to load!
function loadSVG(from) {
	console.log(from);

	var siteName = from.id;	

	console.log("loading: " +siteName);
	var svgContainer = document.getElementById("svg_container");
	var im = document.getElementById("svg_image");

	//adding some sort of timestamp forces browser to redraw image, otherwise wouldn't show up half the time (interesting)
	// + "?time="+Date.now()
	//DECISION: Adding it uses up much more bandwidth for each switch.res
	//	On the other hand it seems to make firefox render the svg properly each time...
	//	not sure if chrome has this issue
	im.data = "plans/" + sites[siteName].sitePlanRes; //CANNOT HAVE A PRECEDING SLASH (think regular unix)
	// var notifier = document.getElementById(siteName).getElementsByClassName("site_name")[0].getElementsByClassName("indicator")[0];
	// notifier.style.backgroundColor = "lightgreen";
	// notifier.parentElement.title = "up to date";
	document.getElementById(currentlySelected).style.backgroundColor = "#E0E0E0";
	currentlySelected = siteName;
	var selector = document.getElementById(currentlySelected);
	selector.style.backgroundColor = "white";
	//we can only do operations on the svg once loaded!
	im.addEventListener("load", function() {
		var linkElm = im.contentDocument.createElementNS("http://www.w3.org/1999/xhtml", "link");
		linkElm.setAttribute("href", "../svgStyling.css");
		linkElm.setAttribute("type", "text/css");
		linkElm.setAttribute("rel", "stylesheet");
		im.contentDocument.getElementsByTagName("defs")[0].appendChild(linkElm);
		console.log(linkElm);
		updateSvgData(currentlySelected);
		orig_width = im.width;
	});
}
