import requests
import os
import json


def pull_in_dependencies(manifest, force=False):
    ''' Handles pulling in dependencies '''
    # Return immediately if there are no dependencies to handle
    if 'dependencies' not in manifest:
        return

    for dependency in manifest['dependencies']:
        if dependency['type'] not in dependency_handlers:
            error = "ERROR: There is no handler for dependency type '{0}'."
            print error.format(dependency['type'])
            return
        else:
            dependency_handlers[dependency['type']](dependency, force)


def file_dependency(dependency, force=False):
    ''' Pull down a file-type dependency '''
    if 'source' not in dependency:
        print 'source for a file-based dependency was not defined'
        return
    if 'filename' not in dependency:
        print 'filename for a file-based dependency was not defined'
        return

    source = dependency['source']
    filename = dependency['filename']

    # Request file
    req = requests.get(source)
    if req.status_code != 200:
        error = "Failed to download dependency source from {0}: {1} {2}"
        print error.format(source, req.status_code, req.reason)
        return

    # Write file
    if os.path.exists(filename) and not force:
        if req.text == open(filename).read():
            print '{0} is up to date'.format(filename)
        else:
            error = "File {0} already exists, use -f flag to force overwrite"
            print error.format(filename)
            return
    else:
        with open(filename, 'w') as fp:
            fp.write(req.text)
            print '{0} downloaded from {1}'.format(filename, source)


def packageurl_dependency(dependency, force=False):
    ''' Pulls down a package via URL '''
    if 'source' not in dependency:
        print 'source for a packageurl-based dependency was not defined'
        return

    source = dependency['source']

    # Get package manifest
    source_manifest = source + '/packilog.json'
    req = requests.get(source_manifest)
    if req.status_code != 200:
        error = "Failed to download dependency manifest from {0}: {1} {2}"
        print error.format(source_manifest, req.status_code, req.reason)
        return

    package_manifest = json.loads(req.text)
    # Recursively handle dependencies
    pull_in_dependencies(package_manifest)

    # Pull in files referenced
    if 'files' in package_manifest:
        for filename in package_manifest['files']:
            sourcepath = '{0}/{1}'.format(source, filename)
            req = requests.get(sourcepath)
            if req.status_code != 200:
                error = "Failed to download dependency source from {0}: {1} {2}"
                print error.format(sourcepath, req.status_code, req.reason)
                return
            if os.path.exists(filename) and not force:
                if req.text == open(filename).read():
                    print '{0} is up to date'.format(filename)
                else:
                    error = "File {0} already exists, use -f flag to force overwrite"
                    print error.format(filename)
                    return
            else:
                with open(filename, 'w') as fp:
                    fp.write(req.text)
                    print '{0} downloaded from {1}'.format(filename, source)


dependency_handlers = {'file': file_dependency,
                       'packageurl': packageurl_dependency}
