from yasuf import Yasuf

y = Yasuf('xoxp-30011478837-30016083441-30011109927-affd3e7e61',
          channel='#general')

@y.handle('test ([0-9]+)', types=[int])
def say_hey(times):
    for i in range(times):
        print('Hey!')
    a = {}
    a[1]
    return "What's up!"

y.run()
