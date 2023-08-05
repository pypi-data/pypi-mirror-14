import os
from chatter_learning import Chatter

chatter = Chatter(database_url='mongodb://127.0.0.1:27017')
chatter.store.drop()
while True:
    testVar = raw_input()
    print chatter.response_to(testVar)