#!/usr/bin/python

import routes    # url recognition system
import routefs   # allows treatment of filesystems as directory structures without worrying about syscalls
from twitter import Twitter   # Twitter Tools

class TwitFS(routefs.RouteFS):
    def __init__(self, *args, **kwargs):
        super(TwitFS, self).__init__(*args, **kwargs)

        # Maps user -> [friends]
        self.user_cache = {}
        self.status_cache = {}
        self.twitter = Twitter()

    def make_map(self):
        m = routes.Mapper()
        m.connect('/', controller = 'list_users')
        m.connect('/{user}', controller = 'list_friends')
        m.connect('/{user}/{friend}', controller = 'list_statuses')
        return m

    def list_users(self, **kwargs):
        return [user
            for user, friends in self.user_cache.iteritems()
            if friends]

    def list_friends(self, user, **kwargs):
        print "Requesting user %s"%user
        if user not in self.user_cache:
            try:
                names = []
                ids = self.twitter.friends.ids(screen_name=user)
                print "Retrieved friend ids for %s"%user
                for id in ids:    # the api should support twitter.users.lookup(user_id=id1,id2...) to grab response in one shot, but this requires authentication. querying one-by-one in the meantime. #TODO this is NOT feasible.
                    names.append(self.twitter.users.lookup(user_id=id)['screen_name'].encode('utf-8'))
                print "Retrieved friend names for %s"%user
                self.user_cache[user] = names
            except:
                self.user_cache[user] = None
        return self.user_cache[user]

    def list_statuses(self, user, friend, **kwargs):
        print "Retrieving status of %s"%friend
        if user not in self.status_cache:
            try:
                status = self.twitter.users.lookup(screen_name=friend)['status']['text'].encode('utf-8')
                print "status = %s"%status
                if status:
                    status += '\n'
                self.status_cache[user] = status
            except:
                self.status_cache[user] = None
                return self.status_cache[user]

if __name__ == '__main__':
    routefs.main(TwitFS)
