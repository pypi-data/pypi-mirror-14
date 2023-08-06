var toggle;

toggle = function(event) {
  var obj, target, tclass;
  obj = $(this);
  if (obj.attr('id') === 'navcontroll') {
    $('article').toggleClass('topspace');
  }
  $('span', obj).toggleClass('hidden');
  target = obj.attr('data-target');
  tclass = obj.attr('data-class');
  $(target).toggleClass(tclass);
  return false;
};

$(function() {
  $('button').on('click', toggle);
  return $('#navcontroll').toggleClass('hidden');
});

//# sourceMappingURL=main.js.map
