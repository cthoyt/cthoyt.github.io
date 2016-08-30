jQuery(function($) {
	$("#rss-feeds-wordpress").rss("http://feeds.feedburner.com/CharlesTapleyHoyt", {
		limit: 2,
		ssl: true,
		dateFormat: 'MMMM Do',
		layoutTemplate: "<div class='feed-container'>{entries}</div>",
		entryTemplate: '<div><a href="{url}">{date} - {title}</a><br/>{first_paragraph} <a class="feed-read-more" href="{url}">Read more</a> {categories}</div>',
		tokens: {
			first_paragraph: function(entry, tokens) {
				// just get the first paragraph (lede), which might be embedded in a div or something
				s = entry['content'].replace(/<(?:.|\n)*?>/gm, '\n')
				s = s.trim()
				s = s.split("\n")[0]
				return s
			},
			categories: function(entry, tokens) {
				r = []
				for (var key in entry["categories"]) {
					cat = entry["categories"][key]["name"]
					ent = '<a class="hashtag" href="https://charlestapleyhoyt.wordpress.com/category/' +  cat + '">#' + cat +  '</a> '
					r.push(ent)
				}
				return r.join("")
			}
		}
	});
	$("#rss-feeds-github").rss("http://feeds.feedburner.com/cthoyt-github", {
		limit: 2,
		ssl: true,
		dateFormat: 'DD.MM.YY',
		layoutTemplate: "<span>{entries}</span>",
		entryTemplate: '{date}<a href="{url}"> {title}</a>',
	});
	$("#rss-feeds-soundcloud").rss("http://feeds.feedburner.com/soundcloud/WUST", {
		limit: 2,
		ssl: true,
		dateFormat: 'DD.MM.YY',
		layoutTemplate: "<span>{entries}</span>",
		entryTemplate: '{date}<a href="{url}"> {title}</a>',
	});
	$(document).bind('mousemove', function(e) {
		if($(window).width() > 768) {
			lp = Math.round(100 * e.pageX / $(window).width())
			tp = Math.round(100 * e.pageY / $(window).height())
			$("section").css("padding-left", lp / 3)
			$("article").css("margin-top", tp / 8)
		} else {
			$("section").css("padding-left", 0)
			$("article").css("margin-top", 0)
		}	
	}); 
		
});
d3.json("http://ws.audioscrobbler.com/2.0/?method=user.getRecentTracks&user=cthoyt&api_key=351ea17a1c0f477bcfd6f093b8474389&format=json&limit=1&nowplaying=true", function(error, da) {
	tune = da.recenttracks.track[0]
	if ("nowplaying" in tune["@attr"]) {
		document.getElementById("nowplaying").innerHTML = '<h4>Now Playing</h4><span><img id="nowplayingimg" src="' + tune.image[0]["#text"] + '"><a href="' + tune.url +  '">'  + tune.name + " - " + tune.artist["#text"] + '</a></span>'
	}
});
