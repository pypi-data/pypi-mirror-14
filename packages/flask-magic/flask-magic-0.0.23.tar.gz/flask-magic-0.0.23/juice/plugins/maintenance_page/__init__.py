
from juice import (View, register_package, abort)

register_package(__package__)

def view(template=None):
    """
    Create the Maintenance view
    Must be instantiated

    import maintenance_view
    MaintenanceView = maintenance_view()

    :param template_: The directory containing the view pages
    :return:
    """
    if not template:
        template = "Juice/Plugin/MaintenancePage/index.html"

    class Maintenance(View):

        @classmethod
        def register(cls, app, **kwargs):
            super(cls, cls).register(app, **kwargs)

            if cls.get_config("APPLICATION_MAINTENANCE_ON"):
                app.logger.info("APPLICATION MAINTENANCE PAGE IS ON")

                @app.before_request
                def on_maintenance():
                    return cls.render_(layout_=template), 503

    return Maintenance

Maintenance = view()