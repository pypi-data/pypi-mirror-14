import json

# Expects units to be a dictionary like:
# { "a": {"depends": ["b", "c"], "value": ...},
#   "b": {"depends": ["c"], "value": ...},
#   "c": {"depends": [], "value": ...},
#   "d": {"depends": ["c"], "value": ...} }
def resolve_depends(units, preresolved=[]):
    for name in units:
        units[name]["depends"] = set(units[name].get("depends", []))
        units[name]["depends"] |= set([u for u in units[name].get("optdepends", []) if u in units])

    # Contains dependencies resolved last round
    resolved = set(preresolved)
    while units:
        # Mark as resolved, to handle next time around
        to_resolve = set()
        for k, v in list(units.items()):
            # Remove dependencies we resolved already
            v["depends"] -= resolved

            # If this has dependencies still, skip it
            if v["depends"]: continue

            # Otherwise, mark this as resolved
            to_resolve.add(k)

            # And yield it to the caller
            yield (k, units.pop(k).get("value", None))

        resolved = to_resolve

        if not resolved:
            # We have not resolved anything this round
            # This means we're stuck

            present = set(units.keys()) | set(preresolved)

            required = set()
            for v in units.values():
                required.update(v["depends"])

            if required - present:
                # There is an unmet dependency
                raise ValueError("Unsatisfied dependencies: " + ", ".join(list(required)))
            else:
                # There is a circular dependency
                raise ValueError("Circular dependency detected")

def load_metadata(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except:
        data = {}

    if "name" not in data:
        data["name"] = os.path.splitext(os.path.basename(path))[0]

    return data

def preload_modules(path, system=False):
    modules = {}
    for path, assets in load_dir(path, True, False):
        if path.endswith(".meta"):
            metadata = load_metadata(path)
            if "name" not in metadata:
                pass

def load_dir(path, include_assets=False, do_import=True):
    sys.path.insert(0, os.path.abspath("."))
    modules = []
    for f in os.listdir(path):
        try:
            if f.startswith(".") or f.endswith("~") or f.endswith("#") or f.startswith("__"):
                continue

            LOG.info("Loading file {}...".format(os.path.join(path, f)))
            name = os.path.splitext(f)[0]

            try:
                if do_import:
                    modules.append((imp.load_source(name, os.path.join(path, f)), None))
                else:
                    modules.append((os.path.join(path, f), None))

            except IsADirectoryError:
                LOG.info("Attempting to load directory {} as a module...".format(
                    os.path.join(path, f)))

                try:
                    if do_import:
                        mod = imp.load_source(name, os.path.join(path, f, '__init__.py'))
                    else:
                        mod = os.path.join(path, f, '__init__.py')
                    assets = None
                    if os.path.exists(os.path.join(path, f, 'assets')) and \
                       os.path.isdir(os.path.join(path, f, 'assets')):
                        assets = os.path.abspath(os.path.join(path, f, 'assets'))

                    modules.append((mod, assets))
                except FileNotFoundError:
                    LOG.error("Unable to load module {}: {} does not exist".format(
                        name, os.path.join(path, f, '__init__.py')))
        except:
            LOG.exception("Exception encountered while loading {}".format(os.path.join(path, f)))

    return modules
