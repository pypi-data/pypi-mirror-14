var Passport = function(){

};

Passport.prototype.init = function(icon_placement){
    // https://atlas.wgbh.org/stash/projects/TOOL/repos/passport/browse
    // authors: Dan Hart, Jonathan Ellenberger
    // publisher: WGBH Foundation
    // last modified date: 3/1/2016

    // summary: loads a list of COVE IDs that are Passport enabled and updates the Passport icon on the page
    // CRON job will create file & copy to S3:
    // "http://s3.amazonaws.com/pbs-ingest/wgbh/passport/cove_list.txt"
    var PLACEMENT = icon_placement;

    if(typeof PLACEMENT === "undefined") {
        PLACEMENT = 'overline';
    }

    if (PLACEMENT != 'overline' && PLACEMENT != 'poster_image') {
        PLACEMENT = 'overline';
    }

    logit("Passport js loaded!")


    var cove_list = "",
        queue_id = [],
        _debug = true,
        _notlive = location.hostname === "localhost" || location.hostname === "dipsy.pbs.org" || location.hostname === "staging.pbs.org" || location.hostname === "127.0.0.1"


    $( document ).ready(function() {

        // ajax call:
        var request = $.get('http://s3.amazonaws.com/pbs-ingest/wgbh/passport/cove_list_special.txt'),
            i

        logit("Sent request")

        request.done(function(result) {

            // assume that the file will contain a JSON object containing an array in
            // the cove_passport_members_only object:

            cove_list = JSON.parse(result).cove_passport_members_only
            logit("Request response received")
            checkAllCoveIDs()
            logit("The queue = " + queue_id)

            for (i=0; i<queue_id.length; i++) {
                addPassportIcon(queue_id[i][0], queue_id[i][1])
            }
            queue_id = []

            // test
            // logit("remove the Passport icon if desired")
            // removePassportIcon($('#remove-test'))

            // test
            // logit("direct call when we know cove_list response is ready ")
            // doPassportEnable(2365340607, $("#direct-cove-ask"))

            // hide em all!
            //$('.passport-icon').hide('slow');

        })
        .fail(function(jqXHR, textStatus, errorThrown) {
          if (textStatus == 'timeout')
            logit('The server is not responding');

          if (textStatus == 'error')
            logit(errorThrown);
            $('#errors').html(errorThrown)
        });

        // EXAMPLE :

        // Example of using a JavaScript query that will first check to see if the list is ready,
        // and add the DOM element to the queue if it is not:

        /*
            if (isPassportEnabled(999)==="NA") {
                doPassportEnable(999, $("#direct-cove-ask1"))
            }

            if (isPassportEnabled(2326265705)==="NA") {
                doPassportEnable(2326265705, $("#direct-cove-ask2"))
            }
        */

        // TESTING :

        /*
        logit("is Testing for video = random, result = " + isPassportEnabled(999) )
        logit("is Testing for video = 2326265705, result = " + isPassportEnabled(2326265705) )
        logit("do Testing for video = random, result = " + doPassportEnable(999, $("#direct-cove-ask1")) )
        */

    });

    function isPassportEnabled(cove_id) {

        // given a cove id, determine if this video is only available to members
        // returns true/false OR "NA"
        // also see doPassportEnable(), which will add requests to a queue

        if (cove_list!="") {
            var response = $.inArray( Number(cove_id) , cove_list) != -1
            logit("(is) COVE id found = " + response)
            return response

        } else {
            logit("(is) The COVE id list is not ready, request was for coveid = " + cove_id)
            return "NA"
        }

    }

    function doPassportEnable(cove_id, el) {

        // given a cove id and DOM element, will add passport element.
        // request will be added to queue for processing if cove list is not ready

        if (cove_list!="") {
            var response = $.inArray( Number(cove_id) , cove_list) != -1
            logit("(do) COVE id found = " + response)
            addPassportIcon(cove_id, el)

        } else {
            logit("(do) The COVE id list is not ready, request was for coveid = " + cove_id)
            queuePassportResponse(cove_id, el )
        }

    }

    function queuePassportResponse(cove_id, el) {

        queue_id.push([cove_id, el])

    }

    function checkAllCoveIDs() {

        var dataset = $("[data-service='pbs_cove']")

        if (dataset.length > 1) {

                dataset.each(function(){
                    logit("multiple ids " + $(this).data('service-id'));
                    addPassportIcon($(this).data('service-id'), $(this));
                });

        } else if (dataset.length === 1) {
            // do one only
            addPassportIcon(dataset.data('coveid'), dataset)
            logit("found one cove ids found on this page " + dataset.data('coveid'))

        } else {
            // none found
            logit("no cove ids found on this page ")
        }

        // this is a test, in case you need to dynamically revert from passport video to open video.
        //removePassportIcon($('[data-coveidx]'))

    }

    function addPassportIcon(cove_id, el) {

        //logit("checking " + cove_id)
        //logit(Array.isArray(cove_list))

        if ( $.inArray( Number(cove_id) , cove_list) != -1 ) {
            stuffPassportIcon(el)
        }
    }

    function stuffPassportIconOverline(el) {
        if ($(el, 'div.stacks-list-module').length==1 && el.hasClass('stacks-instance-module') == false) {
            var parent_div = el.parents('div.grid-block-inner');
            var overline = parent_div.find('.overline');
            overline.append('<div class="passport-icon"></div>');
        } else if (el.hasClass('stacks-instance-module') == true) {
            var overline = el.find('.overline');
            overline.append('<div class="passport-icon"></div>');
        }
    }

    function stuffPassportIconPosterImage(el) {
        var play_icon_container = el.find('.play-icon-container');
        play_icon_container.append('<div class="passport-icon"></div>');
    }

    function stuffPassportIcon(el) {
        console.log(PLACEMENT);
        if (PLACEMENT == 'overline') {
            stuffPassportIconOverline(el);
        }
        else {
            stuffPassportIconPosterImage(el);
        }
    }

    function removePassportIcon(el) {

        logit("remove " + el)
        logit(el.html())

        el.find('.passport-icon').remove()

    }

    function logit(msg) {
        if(window.console && _debug && _notlive){
            console.log(msg);
        }
    }

    return {

        isPassportEnabled: function(cove_id) {
            return isPassportEnabled(cove_id);
        },
        doPassportEnable: function(cove_id, el) {
            doPassportEnable(cove_id, el);
        },
        stuffPassportIcon: function(el) {
            stuffPassportIcon(el);
        },
        removePassportIcon: function(el) {
            removePassportIcon(el);
        }
    }

};

module.exports = Passport;
