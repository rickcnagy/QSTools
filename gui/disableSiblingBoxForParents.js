<script type="text/javascript">

$(window).load(function() {
    var extendTimer = setInterval(function() {
        if (typeof S_ParentTab !== "undefined") {
            clearInterval(extendTimer);
            disableSiblingsBoxForParents();
        }
    }, 50);
});

function disableSiblingsBoxForParents() {
    S_ParentTab.prototype._renderSiblings = extend(
    Rest.get("/sms/v1/self", {}, this, function(returnData) {
        if (returnData.personType === "Parent") {
            S_ParentTab.prototype._renderSiblings = extend(
                    S_ParentTab.prototype._renderSiblings, function() {
                $(".qpwRow:contains(Siblings) .inputBox")
                    .unbind("click")
                    .addClass("readOnly");
            });
        }
    });
}

function extend(oldFunc, newFunc, newFuncIsAfter) {
    newFuncIsAfter = newFuncIsAfter || true;
    return function() {
        if (newFuncIsAfter) {
            var ret = oldFunc.apply(this, arguments);
            newFunc.apply(this, arguments);
            return ret;
        } else {
            newFunc.apply(this, arguments);
            return oldFunc.apply(this, arguments);
        }
    };
}

</script>
