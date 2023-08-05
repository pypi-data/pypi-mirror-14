import json

from flask import redirect, request, session
from flask.ext.jsonpify import jsonify

from .. import preprocessors, responses
from ...database import IntegrityError, NotFoundError


def configure(bp, config, db):

    @bp.route("/campaigns/", methods=["GET"])
    def campaigns_index():
        """
        Returns a list of wikis that have active campaigns.
        """
        info = "Welcome to the campaigns module.  This module provides " + \
               "access to data using a heirachical strategy: 'wikis' have " + \
               "'campaigns', 'campaigns' have 'worksets' and 'worksets' " + \
               "have 'tasks'.  The URL structure looks like this: /campaigns/" + \
               "<wiki>/<campaign_id>/<workset_id>/<task_id>/."
        return jsonify({'info': info,
                        'wikis': db.campaigns.wikis()})

    @bp.route("/campaigns/<wiki>/", methods=["GET"])
    def get_wiki(wiki):
        """
        Returns a list of campaigns available for this particular wiki.
        """
        if 'create' in request.args:
            create_campaign(wiki, request.args['create'])
        else:
            stats = request.args.get('campaigns') == "stats"
            return jsonify(
                {
                    "wiki": wiki,
                    "campaigns": db.campaigns.for_wiki(wiki, stats)
                }
            )

    @bp.route("/campaigns/<wiki>/", methods=["POST"])
    @preprocessors.authenticated
    def create_campaign(wiki, campaign=None):
        """
        Creates a new campaign
        """
        campaign = json.loads(campaign or request.form.get('campaign'))

        return responses.not_implemented("Create campaign")

    @bp.route("/campaigns/<wiki>/<int:campaign_id>/", methods=["GET"])
    def get_campaign(wiki, campaign_id):
        """
        Returns metadata for a campaign or assign a new workset
        """
        if 'assign' in request.args:
            return assign_workset(wiki, campaign_id)

        doc = {}
        if 'tasks' in request.args:
            doc['tasks'] = db.tasks.for_campaign(campaign_id)

        if 'worksets' in request.args:
            stats = request.args.get('worksets') == "stats"
            doc['worksets'] = db.worksets.for_campaign(campaign_id, stats)

        try:
            stats = request.args.get('campaign') == "stats"
            doc['campaign'] = db.campaigns.get(campaign_id, stats)
            return jsonify(doc)
        except NotFoundError as e:
            return responses.not_found(str(e))

    @bp.route("/campaigns/<wiki>/<int:campaign_id>/", methods=["POST"])
    @preprocessors.authenticated
    def assign_workset(wiki, campaign_id):
        """
        Assigns and gathers metadata for a particular workset
        """
        user_id = session['user']['id']

        stats = request.args.get('workset') == "stats"
        try:
            doc = {'workset': db.worksets.assign(campaign_id, user_id, stats)}
        except IntegrityError as e:
            return responses.conflict(str(e))
        except NotFoundError as e:
            return responses.not_found(str(e))

        if 'campaign' in request.args:
            stats = request.args.get('campaign') == "stats"
            try:
                doc['campaign'] = db.campaigns.get(campaign_id, stats)
            except NotFoundError as e:
                return responses.not_found(str(e))

        if 'tasks' in request.args:
            doc['tasks'] = db.tasks.for_workset(doc['workset']['id'])

        return jsonify(doc)

    @bp.route("/campaigns/<wiki>/<int:campaign_id>/<int:workset_id>/", methods=["GET"])
    def get_workset(wiki, campaign_id, workset_id):
        """
        Gathers metadata for a particular workset
        """
        if 'abandon' in request.args:
            return abandon_workset(wiki, campaign_id, workset_id)

        doc = {}
        if 'campaign' in request.args:
            stats = request.args.get('campaign') == "stats"
            try:
                doc['campaign'] = db.campaigns.get(campaign_id, stats)
            except NotFoundError as e:
                return responses.not_found(str(e))

        if 'tasks' in request.args:
            doc['tasks'] = db.tasks.for_workset(workset_id)

        try:
            stats = request.args.get('workset') == "stats"
            doc['workset'] = db.worksets.get(workset_id, stats)
        except NotFoundError as e:
            return responses.not_found(str(e))

        return jsonify(doc)

    @bp.route("/campaigns/<wiki>/<int:campaign_id>/<int:workset_id>/", methods=["DELETE"])
    @preprocessors.authenticated
    def abandon_workset(wiki, campaign_id, workset_id):
        """
        Abandons a workset for a user.
        """
        workset = db.worksets.get(workset_id)

        if workset['user_id'] != session['user']['id']:
            return responses.forbidden(("workset_id={0} is owned by " +
                                        "user_id={1}, but your user_id is {2}")\
                                        .format(workset_id, workset['user_id'],
                                                session['user']['id']))

        db.worksets.abandon(workset_id, session['user']['id'])

        return jsonify({'success': True})


    @bp.route("/campaigns/<wiki>/<int:campaign_id>/<int:workset_id>/<int:task_id>/", methods=["GET"])
    def get_task(wiki, campaign_id, workset_id, task_id):
        """
        Gets a task label
        """
        if 'label' in request.args:
            return label_task(wiki, campaign_id, workset_id, task_id,
                              request.args['label'])

        doc = {}
        if 'campaign' in request.args:
            stats = request.args.get('campaign') == "stats"
            try:
                doc['campaign'] = db.campaigns.get(campaign_id, stats)
            except NotFoundError as e:
                return responses.not_found(str(e))

        if 'workset' in request.args:
            stats = request.args.get('workset') == "stats"
            try:
                doc['workset'] = db.worksets.get(workset_id, stats)
            except NotFoundError as e:
                return responses.not_found(str(e))

        try:
            doc['task'] = db.tasks.get(task_id)
        except NotFoundError as e:
            return responses.not_found(str(e))

        return jsonify(doc)

    @bp.route("/campaigns/<wiki>/<int:campaign_id>/<int:workset_id>/<int:task_id>/",
               methods=["PUT", "POST"])
    @preprocessors.authenticated
    def label_task(wiki, campaign_id, workset_id, task_id, label=None):
        """
        Adds a label to a workset task.
        """
        label = json.loads(label or request.form.get('label'))

        doc = {'label': db.labels.upsert(task_id, session['user']['id'], label)}

        if 'campaign' in request.args:
            stats = request.args.get('campaign') == "stats"
            try:
                doc['campaign'] = db.campaigns.get(campaign_id, stats)
            except NotFoundError as e:
                return responses.not_found(str(e))

        if 'workset' in request.args:
            stats = request.args.get('workset') == "stats"
            try:
                doc['workset'] = db.worksets.get(workset_id, stats)
            except NotFoundError as e:
                return responses.not_found(str(e))

        if 'task' in request.args:
            try:
                doc['task'] = db.tasks.get(task_id)
            except NotFoundError as e:
                return responses.not_found(str(e))

        return jsonify(doc)

    return bp
