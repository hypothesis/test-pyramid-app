from glob import glob

bind = "0.0.0.0:9800"
reload = True
reload_extra_files = glob("test_pyramid_app/templates/**/*", recursive=True)
timeout = 0
