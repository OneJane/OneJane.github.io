$(function(){var t=$(".recent-post-item img").not(".no-fancybox");0===t.length&&(t=$("#post-content img").not(".no-fancybox"));for(var a=0;a<t.length;a++){var o=$('<a href="'+t[a].src+'" data-fancybox="group" data-caption="'+t[a].alt+'" class="fancybox"></a>'),n=t[a].alt,c=$(t[a]).wrap(o);n&&c.after('<div class="img-alt">'+n+"</div>")}$().fancybox({selector:"[data-fancybox]",loop:!0,transitionEffect:"slide",buttons:["share","slideShow","fullScreen","download","thumbs","close"]});var e=$(".gallery-item"),i=[];e.each(function(t,a){i.push({src:$(a).data("url"),opts:{caption:$(a).data("title")}})}),e.on("click",function(){return $.fancybox.open(i,{loop:!0,transitionEffect:"slide"},e.index(this)),!1})});