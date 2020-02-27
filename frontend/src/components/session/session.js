var Session = (function () {
    var getSession = function () {
        var value = "; " + document.cookie;
        var parts = value.split("; cas-session:");

        if (parts.length === 2)
            return parts.pop().split(";").shift();
    };

    var setSession = function (id) {
        document.cookie = "cas-session:" + id;
    };

    var deleteSession = function () {
        document.cookie = "cas-session:";
    }

    return {
        getSession: getSession,
        setSession: setSession,
    }

})();

export default Session;
