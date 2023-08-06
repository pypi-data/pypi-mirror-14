
/*
 *     The below variables was declared in
 *         colab/colab/plugins/noosfero/templates/proxy/noosfero.html:
 *             community         - community name from the noosfero
 *             */

$(transform_tags);

function transform_tags() {
    discussion_tag();
    feed_gitlab_tag();
}

function feed_gitlab_tag() {
  var $tag = $('#repository-feed-tab');
  var request_path = '/spb/gitlab_activity/?community='+community;
  $tag.load(request_path)
}

function discussion_tag() {
  var $tag = $('#discussions-tab');
  var request_path = '/spb/mail_list/?community='+community;
  $tag.load(request_path);
}
