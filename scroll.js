$(function(){var r=0;function e(e){var i;try{i=$(e)}catch(t){i=$(decodeURI(e))}i.velocity("stop").velocity("scroll",{duration:500,easing:"easeInOutQuart"})}$(".toc-child").hide(),$(window).scroll(throttle(function(t){var e,i,o,a,s,n=$(this).scrollTop();isMobile()||(o=n,a=$("#content-outer").height(),s=(s=$(window).height())<a?a-s:$(document).height()-s,s=o/s,s=100<(s=Math.round(100*s))?100:s<=0?0:s,$(".progress-num").text(s),$(".sidebar-toc__progress-bar").velocity("stop").velocity({width:s+"%"},{duration:100,easing:"easeInOutQuart"}),e=n,0!==$(".toc-link").length&&(l=$("#post-content").find("h1,h2,h3,h4,h5,h6"),i="",l.each(function(){var t=$(this);e>t.offset().top-25&&(i="#"+$(this).attr("id"))}),""===i&&($(".toc-link").removeClass("active"),$(".toc-child").hide()),"5"===GLOBAL_CONFIG.hexoVersion[0]&&(i=encodeURI(i)),c=$(".toc-link.active"),i&&c.attr("href")!==i&&(function(t){window.history.replaceState&&t!==window.location.hash&&window.history.replaceState(void 0,void 0,t)}(i),$(".toc-link").removeClass("active"),(l=$('.toc-link[href="'+i+'"]')).addClass("active"),function(t){t.is(":visible")||t.velocity("stop").velocity("transition.fadeIn",{duration:500,easing:"easeInQuart"})}((l=0<(c=l.parents(".toc-child")).length?c.last():l).closest(".toc-item").find(".toc-child")),l.closest(".toc-item").siblings(".toc-item").find(".toc-child").hide())));var c,l,l=(l=r<(c=n),r=c,l);56<n?(l?$("#page-header").hasClass("visible")?$("#page-header").removeClass("visible"):console.log():$("#page-header").hasClass("visible")?console.log():$("#page-header").addClass("visible"),$("#page-header").addClass("fixed"),"0"===$("#go-up").css("opacity")&&$("#go-up").velocity("stop").velocity({translateX:-30,rotateZ:360,opacity:1},{easing:"easeOutQuart",duration:200})):(0===n&&$("#page-header").removeClass("fixed").removeClass("visible"),$("#go-up").velocity("stop").velocity({translateX:0,rotateZ:180,opacity:0},{easing:"linear",duration:200}))},50,100)),$("#go-up").on("click",function(){$("body").velocity("stop").velocity("scroll",{duration:500,easing:"easeOutQuart"})}),$("#post-content").find("h1,h2,h3,h4,h5,h6").on("click",function(t){e("#"+$(this).attr("id"))}),$(".toc-link").on("click",function(t){t.preventDefault(),e($(this).attr("href"))})});