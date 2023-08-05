from score.init import ConfiguredModule, parse_bool
from webob import Request


defaults = {
    'pregenerate-assets': False,
}


def init(confdict):
    conf = defaults.copy()
    conf.update(confdict)
    conf['pregenerate-assets'] = parse_bool(conf['pregenerate-assets'])
    return Configured{ucname}Module(conf['pregenerate-assets'])


class Configured{ucname}Module(ConfiguredModule):

    def __init__(self, pregenerate_assets):
        import {name}
        super().__init__({name})
        self.pregenerate_assets = pregenerate_assets

    def _finalize(self, ctx, http, tpl, js, css):
        import {name}.db
        tpl.renderer.add_global('html', 'db', {name}.db)
        if self.pregenerate_assets:
            with ctx.Context() as ctx:
                ctx.http = http.create_ctx_member(Request.blank('/'))
                http.route('start').handle(ctx)
