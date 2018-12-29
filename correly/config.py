from vyper import v


def init_config():
    v.set_config_name('correly')
    v.add_config_path('/etc/correly/')
    v.add_config_path('$HOME/.correly')
    v.add_config_path('.')
    v.read_in_config()
