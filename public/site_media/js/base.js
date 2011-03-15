function getViewPortHeight(){
 var viewportheight;
  if (typeof window.innerWidth != 'undefined')
 {
      viewportheight = window.innerHeight
      return viewportheight;
 }
  else if (typeof document.documentElement != 'undefined'
     && typeof document.documentElement.clientWidth !=
     'undefined' && document.documentElement.clientWidth != 0)
 {
       viewportheight = document.documentElement.clientHeight;
       return viewportheight;
 }
 else
 {
       viewportheight = document.getElementsByTagName('body')[0].clientHeight;
       return viewportheight;
 }

}

function adjustFooterPos()
{ 
  var min_height = getViewPortHeight() - 254;
  $('#table').css({'height': min_height + 'px'});
}

window.onresize = function(){
   adjustFooterPos();
}