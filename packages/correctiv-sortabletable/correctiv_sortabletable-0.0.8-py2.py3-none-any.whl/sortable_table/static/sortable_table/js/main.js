window.sortableTable = (function(){
  'use strict';
  var defaultCellColor = '#333';
  var whiteCellColor = '#fff';

  var getValue = function(el) {
    var tdText = el.getAttribute('data-sort') || el.textContent || el.innerText || '';
    return Number(tdText);
  };

  var colourColumn = function(table, col, settings) {
    var vals = [], i, td, tdText, val;
    var trs = table.getElementsByTagName('tr');
    var min = Infinity, max = -Infinity;
    var domain = settings.domain;
    var values = [];
    var offset = 0;
    var t = function(x) {return x;};
    if (settings.logscale) {
      t = function(x) {return Math.LOG10E * Math.log(Math.abs(x)) * Math.sign(x);};
    }
    if (domain === undefined) {
      for (i = 1; i < trs.length; i += 1) { // Skip header
        td = trs[i].getElementsByTagName('td')[col];
        val = t(getValue(td));
        values.push(val);
        min = Math.min(min, val);
        max = Math.max(max, val);
      }
      domain = [min, max];
    }
    if (settings.midpoint !== undefined) {
      domain = [domain[0], settings.midpoint, domain[1]];
    }
    if (settings.reversed) {
      domain = domain.reverse();
    }
    var colorScale = chroma.scale(settings.scale).mode('lab').domain(domain);
    for (i = 1; i < trs.length; i += 1) { // Skip header
      td = trs[i].getElementsByTagName('td')[col];
      val = t(getValue(td));
      var backgroundColor = colorScale(val).hex();
      td.style.backgroundColor = backgroundColor;
      // Check contrast
      if (chroma.contrast(backgroundColor, defaultCellColor) < 4.5) {
        td.style.color = whiteCellColor;
      }
    }
  };

  var sortableTable = function(table, settings) {
    settings.scale = settings.scale || 'OrRd';
    var columns = settings.columns;
    for (var i = 0; i < columns.length; i += 1) {
      if (!columns[i].text && !columns[i].html) {
        colourColumn(table, i, {
          scale: columns[i].scale || settings.scale,
          domain: columns[i].domain,
          midpoint: columns[i].midpoint,
          reversed: columns[i].reversed,
          logscale: columns[i].logscale,
        });
      }
    }
    new Tablesort(table, {descending: !settings.ascending});
  };

  return sortableTable;
}());
