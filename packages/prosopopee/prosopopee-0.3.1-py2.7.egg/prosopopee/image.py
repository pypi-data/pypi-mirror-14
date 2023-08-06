class Image(object):
    base_dir = ""
    target_dir = ""

    def __init__(self, options):
        # assuming string
        if not isinstance(options, dict):
            options = {"name": options}
        self.options = options.copy()  # used for caching, if it's modified -> regenerate
        self.options.update(gm_settings)

    @property
    def name(self):
        return self.options["name"]

    @property
    def quality(self):
        return self.options["quality"]

    @property
    def autoorient(self):
        return self.options["auto-orient"]

    def copy(self):
        source, target = os.path.join(self.base_dir, self.name), os.path.join(self.target_dir, self.name)

        # XXX doing this DOESN'T improve perf at all (or something like 0.1%)
        # if os.path.exists(target) and os.path.getsize(source) == os.path.getsize(target):
            # print "Skipped %s since the file hasn't been modified based on file size" % source
            # return ""
        if not self.autoorient:
            shutil.copyfile(source, target)
            print source, "->", target
        else:
            command = "gm convert %s -strip -auto-orient %s" % (source, target)
            print command
            os.system(command)

        return ""

    def generate_thumbnail(self, gm_geometry):
        thumbnail_name = self.name.split(".")
        thumbnail_name[-2] += "-%s" % gm_geometry
        thumbnail_name = ".".join(thumbnail_name)

        source, target = os.path.join(self.base_dir, self.name), os.path.join(self.target_dir, thumbnail_name)

        if CACHE.thumbnail_needs_to_be_generated(source, target, self):
            gm_options = ""
            if self.autoorient:
                gm_options = "-auto-orient"
            command = "gm convert %s -strip %s -resize %s -quality %s %s" % (source, gm_options, gm_geometry, self.quality, target)
            print command
            os.system(command)
            CACHE.cache_thumbnail(source, target, self)
        else:
            print "skipped %s since it's already generated (based on source unchanged size and images options set in your gallery's settings.yaml)" % target

        return thumbnail_name

    def __repr__(self):
        return self.name


