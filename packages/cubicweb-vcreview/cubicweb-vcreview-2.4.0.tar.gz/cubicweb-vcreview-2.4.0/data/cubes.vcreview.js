/*
 *  :organization: Logilab
 *  :copyright: 2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
 *  :contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
 */

cw.cubes.vcreview = new Namespace('cw.cubes.vcreview');


/* this function is called on to add activity from inlined form
 *
 * It calls the [add|eid]_activity method on the jsoncontroller and [re]load
 * only the view for the added or edited activity
 */
function addActivity(eid, parentcreated, context) {
    validateForm(
	'has_activityForm' + eid, null,
	function(result, formid, cbargs) {
	    if (parentcreated) {
		// reload the whole section
		reloadCtxComponentsSection(context, result[2].eid, eid);
	    } else {
		// only reload the activity component
		reload('vcreview_activitysection' + eid, 'vcreview.activitysection',
		       'ctxcomponents', null, eid);
	    };
	});
}

$(function () {
    /* mark task as done */
    $(document).on('click', '.vcreview_task .task_is_done', function (evt) {
        var $mynode = $(evt.currentTarget),
            $parentnode = $mynode.parents('.vcreview_task'),
            eid = $parentnode.data('eid'),
            d = asyncRemoteExec('vcreview_change_state', eid);
        d.addCallback(function () {
            $('.vcreview_task[data-eid=' + eid + ']').each(function () {
                var params = ajaxFuncArgs('render', null, 'views', 'vcreview.task-view', eid);
                $(this).loadxhtml(AJAX_BASE_URL, params, null, 'swap');
            });
        });
        return false;
    });
    /* add activity */
    $(document).on('click', '.cwjs-vcreview-add-activity', function (evt) {
        var $mynode = $(evt.currentTarget),
            $parentnode = $mynode.parents('.vcreview_activitysection'),
            eid = $mynode.data('eid') || null,
            params = $mynode.data('params'),
            form = $mynode.data('form'),
            args = ajaxFuncArgs('render', form, 'views', 'vcreview.addactivityform', eid, params);
        $parentnode.loadxhtml('ajax', args, 'GET', 'append');
        return false;
    });
});


jQuery.extend(cw.cubes.vcreview, {
    /*
     * Make an ajax call to retreive the diff.
     */
    getDiff: function(rev, current) {
        data = {'rev1': rev,
                'rev2': current,
                'vid': 'vcreview.patch.revisions_diff'
        };
        $.get(BASE_URL, data, function(response) {
            $('#diff-div').html(response);
        }) ;
        $('.list-group-item').removeClass('list-group-item-danger', 'list-group-item-success');
        $('#rev-' + rev).addClass('list-group-item-danger');
        $('#rev-' + current).addClass('list-group-item-success');
    },


    /*
     * Add a trigger to the compare link.
     *
     * Its arguments are:
     *
     * `eids`, a list of eids of the patch revisions.
     * The current revision's eid is at index 0.
     */
    addClickTrigger: function(eids) {
        var current = eids[0];
        $('.icon-diff').each(function (i){
            $(this).click(function() {
                cw.cubes.vcreview.getDiff(eids[i+1], current);
            });
        });
    }
});
