# Here go your api methods.
import time

@auth.requires_signature()
def add_post():
    post_id = db.post.insert(
        post_title=request.vars.post_title,
        post_price=request.vars.post_price,
        post_condition=request.vars.post_condition,
        post_category=request.vars.post_category
    )
    print request.vars.post_price;
    print request.vars.post_title;
    # We return the id of the new post, so we can insert it along all the others.
    return response.json(dict(post_id=post_id))

@auth.requires_signature()
def edit_post():
 db(db.post.id == request.vars.post_id).update(
     post_title = request.vars.post_title,
     post_content = request.vars.post_content,
 )

@auth.requires_signature()
def edit_comment():
    db(db.comments.id == request.vars.id).update(
        body = request.vars.body,
    )
    time.sleep(2)

def get_post_list():
    results = []
    user = None;
    sort_by = request.vars.sortBy
    if auth.user is None:
        user = None;
        print user
        print 'hello'
        # Not logged in.
        rows = db().select(db.post.ALL, orderby=~db.post.post_time)
        for row in rows:
            results.append(dict(
                id=row.id,
                post_title=row.post_title,
                post_content=row.post_content,
                post_author=row.post_author,
                post_price = row.post_price,
                post_condition = row.post_condition,
                post_category = row.post_category,
                post_edition = row.post_category,
                thumb = None,
            ))
    else:
        user = auth.user.email;
        print user
        # Logged in.
        rows = db().select(db.post.ALL, db.thumb.ALL,
                            left=[
                                db.thumb.on((db.thumb.post_id == db.post.id) & (db.thumb.user_email == auth.user.email)),
                            ],
                            orderby=~db.post.post_time)
        for row in rows:
            results.append(dict(
                id=row.post.id,
                post_title=row.post.post_title,
                post_content=row.post.post_content,
                post_author=row.post.post_author,
                post_price = row.post.post_price,
                post_condition = row.post.post_condition,
                post_category = row.post.post_category,
                post_edition = row.post.post_edition,
                thumb = None if row.thumb.id is None else row.thumb.thumb_state,
            ))
    # For homogeneity, we always return a dictionary.
    newlist = sorted(results, key=lambda k: k[sort_by])
    return response.json(dict(post_list=newlist, user_email=user))

def get_comments():
    comments = db(db.comments.post_id == request.vars.id).select()
    return response.json(dict(comments=comments))

def set_comments():
    postID = int(request.vars.post_id)
    bodyText = request.vars.body
    new_comment_id = db.comments.insert(
        post_id = postID,
        body = bodyText
    )
    return response.json(dict(new_comment_id = new_comment_id))

def get_logged_in_user():
   user = None if auth.user == None else auth.user.email
   print auth;
   return response.json(dict(user = user))
