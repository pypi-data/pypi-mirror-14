def pocker_env(dict):
    """
    cnt_opts.env need list of strings as arguments.
    >> ['NEW_ENV_VAR=value', 'ENV_VAR_FROM_HOST']

    Filter transforms dict to list appropriate for cnt_opts.env:
    >> pocker_env({'GET_ENV_FROM_HOST': None}) == [u'GET_ENV_FROM_HOST']
    >> pocker_env({'ONE': 'one', 'TWO': 'two'}) == [u'ONE=one', u'TWO=two']

    Usage example:
      pocker_cnt:
        ...
        cnt_opts:
          env: "{{ {
                  'GET_ENV_FROM_HOST': None,
                  'ONE': 'one',
                }|pocker_env }}"
        ...
    """
    envs = []
    for key, val in dict.iteritems():
      envs.append(unicode(key)) if val is None else envs.append(u"{0}={1}".format(key, val))
    return envs

class FilterModule(object):
     def filters(self):
         return {
             'pocker_env': pocker_env,
          }
