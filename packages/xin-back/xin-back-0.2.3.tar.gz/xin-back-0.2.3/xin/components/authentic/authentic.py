from autobahn.twisted.wamp import ApplicationSession


class AuthenticSession(ApplicationSession):

    def onJoin(self, details):

        def authenticate(realm, authid, details):
            ticket = details['ticket']
            print("WAMP-Ticket dynamic authenticator invoked: realm='{}', "
                  "authid='{}', ticket='{}'".format(realm, authid, ticket))

            # Fake auth for the moment, ticket is role !
            return ticket

        return self.register(authenticate, 'xin.authentic.authenticate')
        print("WAMP-Ticket dynamic authenticator registered!")
