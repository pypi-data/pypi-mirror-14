'use strict';

Object.defineProperty(exports, '__esModule', {
  value: true
});
exports['default'] = calculateNodeHeight;
/**
 * calculateNodeHeight(uiTextNode, useCache = false)
 */

var HIDDEN_TEXTAREA_STYLE = '\n  height:0;\n  visibility:hidden;\n  overflow:hidden;\n  position:absolute;\n  z-index:-1000;\n  top:0;\n  right:0\n';

var SIZING_STYLE = ['letter-spacing', 'line-height', 'padding-top', 'padding-bottom', 'font-family', 'font-weight', 'font-size', 'text-transform', 'width', 'padding-left', 'padding-right', 'border-width', 'box-sizing'];

var computedStyleCache = {};
var hiddenTextarea = undefined;

function calculateNodeHeight(uiTextNode) {
  var useCache = arguments[1] === undefined ? false : arguments[1];
  var minRows = arguments[2] === undefined ? null : arguments[2];
  var maxRows = arguments[3] === undefined ? null : arguments[3];

  if (!hiddenTextarea) {
    hiddenTextarea = document.createElement('textarea');
    document.body.appendChild(hiddenTextarea);
  }

  // Copy all CSS properties that have an impact on the height of the content in
  // the textbox

  var _calculateNodeStyling = calculateNodeStyling(uiTextNode, useCache);

  var sizingStyle = _calculateNodeStyling.sizingStyle;
  var sumVerticalPaddings = _calculateNodeStyling.sumVerticalPaddings;

  // Need to have the overflow attribute to hide the scrollbar otherwise
  // text-lines will not calculated properly as the shadow will technically be
  // narrower for content
  hiddenTextarea.setAttribute('style', sizingStyle + ';' + HIDDEN_TEXTAREA_STYLE);

  hiddenTextarea.value = uiTextNode.value;
  var height = hiddenTextarea.scrollHeight - sumVerticalPaddings;
  var minHeight = -Infinity;
  var maxHeight = Infinity;

  if (minRows !== null || maxRows !== null) {
    // measure height of a textarea with a single row
    hiddenTextarea.value = 'x';
    var singleRowHeight = hiddenTextarea.scrollHeight - sumVerticalPaddings;
    if (minRows !== null) {
      minHeight = singleRowHeight * minRows;
      height = Math.max(minHeight, height);
    }
    if (maxRows !== null) {
      maxHeight = singleRowHeight * maxRows;
      height = Math.min(maxHeight, height);
    }
  }
  return { height: height, minHeight: minHeight, maxHeight: maxHeight };
}

function calculateNodeStyling(node) {
  var useCache = arguments[1] === undefined ? false : arguments[1];

  var nodeRef = node.getAttribute('id') || node.getAttribute('data-reactid') || node.getAttribute('name');

  if (useCache && computedStyleCache[nodeRef]) {
    return computedStyleCache[nodeRef];
  }

  var compStyle = window.getComputedStyle(node);

  var sumPaddings = 0;

  // If the textarea is set to border-box, it's not necessary to
  // subtract the padding.
  if (compStyle.getPropertyValue('box-sizing') !== 'border-box' && compStyle.getPropertyValue('-moz-box-sizing') !== 'border-box' && compStyle.getPropertyValue('-webkit-box-sizing') !== 'border-box') {
    sumPaddings = parseFloat(compStyle.getPropertyValue('padding-bottom')) + parseFloat(compStyle.getPropertyValue('padding-top'));
  }

  var nodeInfo = {
    sizingStyle: SIZING_STYLE.map(function (name) {
      return '' + name + ':' + compStyle.getPropertyValue(name);
    }).join(';'),
    sumVerticalPaddings: sumPaddings
  };

  if (useCache && nodeRef) {
    computedStyleCache[nodeRef] = nodeInfo;
  }
  return nodeInfo;
}
module.exports = exports['default'];
