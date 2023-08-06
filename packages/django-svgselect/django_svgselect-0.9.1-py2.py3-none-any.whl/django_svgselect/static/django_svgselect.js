if(Element.prototype.removeClass == undefined) {
    Element.prototype.removeClass = function (remove) {
        var newClassName = "";
        var i;
        var classes = this.getAttribute('class').split(" ");
        for (i = 0; i < classes.length; i++) {
            if (classes[i] !== remove) {
                newClassName += classes[i] + " ";
            }
        }
        this.setAttribute('class', newClassName);
    }
}

if(Element.prototype.addClass == undefined) {
    Element.prototype.addClass = function (add) {
        var classes = this.getAttribute('class').split(" ");
        var newClasses = "";
        for(var i = 0; i < classes.length; i++) {
            if (classes[i] == add) {
                //class is already here
                return;
            }
            newClasses += classes[i] + " ";
        }
        this.setAttribute('class', newClasses + add);
    }
}

HTMLSelectElement.prototype.convertToSvg = function(svgId) {
    var svgElement = document.getElementById(this.id + '-svg');
    var options = this.options;
    for(var i=0; i < options.length; i++) {
        //Find the SVG item fo this option, if there is one.
        var item = svgElement.querySelector("#" + options[i].value);
        if(item == undefined) {
            console.log("Select option without corresponding id in SVG: " + options[i].value);
            continue;
        }
        item.addClass('svg-select-option');
        if(options[i].selected) {
            //item.setAttribute('class', 'selected');
            item.addClass('selected');
        }

        item.addEventListener('click', function() {
            for(var i=0; i < options.length; i++) {
                if(options[i].value == this.id) {
                    if(options[i].selected) {
                        this.removeClass('selected');
                    } else {
                        this.addClass('selected');
                    }
                    options[i].selected = !options[i].selected;
                    return;
                }
            }
        });
    }

}

//var selectlist = document.getElementById('jason');
//var svg = document.getElementById('jason-svg');
////selectlist.setAttribute('style', 'display: none;');
//var options = selectlist.options;
//
//for(var i=0; i < options.length; i++) {
//    //Find the SVG item fo this option, if there is one.
//    var item = svg.querySelector("#" + options[i].value);
//    if(item == undefined) {
//        console.log("Select option without corresponding id in SVG: " + options[i].value);
//        continue;
//    }
//    console.log(item);
//    item.addClass('svg-select-option');
//    if(options[i].selected) {
//        //item.setAttribute('class', 'selected');
//        item.addClass('selected');
//    }
//
//    item.addEventListener('click', function() {
//        for(var i=0; i < selectlist.options.length; i++) {
//            if(selectlist.options[i].value == this.id) {
//                if(selectlist.options[i].selected) {
//                    this.removeClass('selected');
//                } else {
//                    this.addClass('selected');
//                }
//                selectlist.options[i].selected = !selectlist.options[i].selected;
//                return;
//            }
//        }
//    });
//}