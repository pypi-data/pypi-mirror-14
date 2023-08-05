# -*- coding: utf-8 -*-
# flake8: noqa
"""
Inspector development stuff

DO NOT COMMIT
"""
import os
import json
import boussole

from boussole.exceptions import CircularImport
from boussole.inspector import ScssInspector

class CatchedRuntimeError(CircularImport):
    pass

def shortpath(path, base_dir):
    if path.startswith(base_dir):
        return path[len(base_dir):]
    return path

def shorten_paths_map(paths_map, base_dir):
    new_map = {}
    for k,v in paths_map.items():
        new_map[shortpath(k, base_dir)] = [shortpath(item, base_dir) for item in v]
    return new_map

def shorten_paths_list(paths_list, base_dir):
    return [shortpath(k, base_dir) for k in paths_list]
    
class ComplexEncoder(json.JSONEncoder):
    """
    Allow to encode properly some objet types
    """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

# For some development debug
if __name__ == "__main__":
    
    boussole_dir = os.path.dirname(boussole.__file__)
    fixtures_dir = os.path.normpath(os.path.join(os.path.abspath(boussole_dir), '..', 'tests', 'data_fixtures'))
    sample_path = os.path.join(fixtures_dir, 'sample_project')
    library1_path = os.path.join(fixtures_dir, 'library_1')
    library2_path = os.path.join(fixtures_dir, 'library_2')
    library_paths = [library1_path, library2_path]
    
    inspector = ScssInspector()
    
    sources = [
        os.path.join(sample_path, 'main_basic.scss'),
        os.path.join(sample_path, 'main_syntax.scss'),
        os.path.join(sample_path, 'main_commented.scss'),
        os.path.join(sample_path, 'main_depth_import-1.scss'),
        os.path.join(sample_path, 'main_depth_import-2.scss'),
        os.path.join(sample_path, 'main_depth_import-3.scss'),
        os.path.join(sample_path, 'main_with_subimports.scss'),
        os.path.join(sample_path, 'main_using_libs.scss'),
        os.path.join(sample_path, 'main_circular_0.scss'),
        os.path.join(sample_path, 'main_circular_1.scss'),
        os.path.join(sample_path, 'main_circular_2.scss'),
        os.path.join(sample_path, 'main_circular_3.scss'),
        os.path.join(sample_path, 'main_circular_4.scss'),
        os.path.join(sample_path, 'main_circular_bridge.scss'),
        os.path.join(sample_path, 'main_circular_5.scss'),
    ]
    
    basic_sourcepath = os.path.join(sample_path, 'main_basic.scss')
    depth1_sourcepath = os.path.join(sample_path, 'main_depth_import-1.scss')
    depth2_sourcepath = os.path.join(sample_path, 'main_depth_import-2.scss')
    depth3_sourcepath = os.path.join(sample_path, 'main_depth_import-3.scss')
    subimports_sourcepath = os.path.join(sample_path, 'main_with_subimports.scss')
    usinglibs_sourcepath = os.path.join(sample_path, 'main_using_libs.scss')
    circular0_sourcepath = os.path.join(sample_path, 'main_circular_0.scss')
    circular1_sourcepath = os.path.join(sample_path, 'main_circular_1.scss')
    circular2_sourcepath = os.path.join(sample_path, 'main_circular_2.scss')
    circular3_sourcepath = os.path.join(sample_path, 'main_circular_3.scss')
    circular4_sourcepath = os.path.join(sample_path, 'main_circular_4.scss')
    circularbridge_sourcepath = os.path.join(sample_path, 'main_circular_bridge.scss')
    circular5_sourcepath = os.path.join(sample_path, 'main_circular_5.scss')
    vendor_sourcepath = os.path.join(sample_path, '_vendor.scss')
    webfont_sourcepath = os.path.join(sample_path, 'components/_webfont.scss')
    icons_sourcepath = os.path.join(sample_path, 'components/_webfont_icons.scss')
    
    results = inspector.inspect(*sources, library_paths=library_paths)
    
    # Display maps from inspection
    print "-"*80
    print "Sources that import other sources (_CHILDREN_MAP)"
    print "-"*80
    
    print json.dumps(shorten_paths_map(inspector._CHILDREN_MAP, sample_path+'/'), indent=4)
    print
    
    
    print
    print "-"*80
    print "Sources that are imported by other sources (_PARENTS_MAP)"
    print "-"*80
    
    print json.dumps(shorten_paths_map(inspector._PARENTS_MAP, sample_path+'/'), indent=4, cls=ComplexEncoder)
    print
    
    print "~"*200
    
    def display_children_process(sourcepath):
        print
        print "-"*80
        print "(inspector.children) They are imported by:", shortpath(sourcepath, sample_path+'/')
        print "-"*80
        
        try:
            deps = list(inspector.children(sourcepath))
        except CatchedRuntimeError:
            print "[!] CatchedRuntimeError error has been raised [!]"
        except CircularImport:
            print "[!] CircularImport error has been raised [!]"
        else:
            print json.dumps(shorten_paths_list(deps, sample_path+'/'), indent=4)
            print
    
    def display_parents_process(sourcepath):
        print
        print "-"*80
        print "(inspector.parents) They are imported by:", shortpath(sourcepath, sample_path+'/')
        print "-"*80
        
        try:
            deps = list(inspector.parents(sourcepath))
        except CatchedRuntimeError:
            print "[!] CatchedRuntimeError error has been raised [!]"
        except CircularImport:
            print "[!] CircularImport error has been raised [!]"
        else:
            print json.dumps(shorten_paths_list(deps, sample_path+'/'), indent=4)
            print
    
    
    ## Basic sample
    #display_children_process(basic_sourcepath)
    
    #print "~"*200
    
    ## Depth sample
    #display_children_process(depth3_sourcepath)
    
    #print "~"*200
    
    ## 
    #display_children_process(usinglibs_sourcepath)
    
    #print "~"*200
    
    ## Some test for case 1>2
    #display_children_process(circular1_sourcepath)
    
    #print "~"*200
    
    ## Some test for case 3>bridge>4
    #display_children_process(circular3_sourcepath)
    
    #print "~"*200
    
    ## Final case for sub circular import
    #display_children_process(circular5_sourcepath)
    
    #print "~"*200
    
    ## Self circular import
    #display_children_process(circular0_sourcepath)
    
    print "~"*200
    
    # ...
    display_parents_process(vendor_sourcepath)
    display_parents_process(icons_sourcepath)
