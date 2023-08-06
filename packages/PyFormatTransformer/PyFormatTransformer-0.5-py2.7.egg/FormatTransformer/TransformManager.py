# Introduction
# ============
# 
# This file demonstrates an ontology-driven transformation between file
# formats as discussed in Hester (2016).  In order to operate it one
# needs format adapters (and dependencies) written in
# Python and matching the expected API (see documentation);
# (ii) the dREL dictionary also provided; (iii) the PyCIFRW package (for dREL transformations).
# Transformation is driven by a list of canonical names (dataname
# bundle).  A generic adapter object is initialised
# with this information. ::

from CifFile import CifDic

# dREL configuration
# ==================
# 
# In order to use our dREL transformer, we must create an object that
# can access our input file with a Python '__getitem__', 'has_key' and
# 'GetKeyedSemanticPacket' method (see section "Configuration" in
# py_from_ast.nw.).  This object will recursively call itself to access
# any missing data.  We define a class which we initialise with the
# relevant format adapter.  
# 
# We also provide a filter option, which allows us to restrict returned
# values to those that match the filter criteria.  This ensures that the
# dREL methods only operate on those rows that match the criteria.
# 
#  ::

class GenericInput(dict):
    """A class that can be fed to dREL for recursive evaluation"""
    def __init__(self,input_module,dictionary,*args,**kwargs):
        """input_module is a format adapter that has method 
        get_by_name and is already initialised by file and blockname"""
        super(GenericInput,self).__init__(*args,**kwargs)
        self.input_module = input_module
        self.dictionary = dictionary
        # dummy items to make derive_item happy
        self.provide_value = None
        self.loops = []
        self.filters = {}
        self.setup_translation()

    def __getitem__(self,name,use_drel=True):
        """Return an item as standard type"""
        print 'DEBUG: Accessing %s' % name
        if super(GenericInput,self).has_key(name):  #stored already
            print 'Providing cached value for %s' % (name)
            inval = super(GenericInput,self).__getitem__(name)
            if not isinstance(inval,list):
                print 'WARNING: non-list value stored for %s:%s' %(name,`inval`)
            return inval
        our_type = self.dictionary[name]['_type.contents']
        our_units = self.dictionary[name].get('_units.code',None)
        generic_name = self.generic_name_table[name]
        result = self.input_module.get_by_name(generic_name,our_type,our_units)
        if len(self.filters)>0:
            result = self.apply_filters(generic_name,result)
        if result is None and use_drel:  #need to use dREL fu
            print "=== Deriving %s as not found in datafile" % name
            result = self.dictionary.derive_item(name,self,allow_defaults=False)
            if result is None:
                print '===Trying to derive %s again with defaults allowed' % name
                result = self.dictionary.derive_item(name,self,allow_defaults=True)
            if result is not None and not (isinstance(result,list) and None in result):
                self[name] = result
                print "===Successfully derived %s = %s" % (name,result)
            else:
                print 'Warning: derivation of %s failed' % name
        elif result is not None:
            print "Stored %s for %s" % (result,name)
            self[name] = result
        return result
        
    def __setitem__(self,name,value):
        """Set a value, after checking. We do not touch the underlying input file.
        All values should be lists at the top level."""
        if value is None or isinstance(value,list) and None in value:
            raise ValueError, "Attempt to set None value for %s" % name
        if not hasattr(value,'__iter__'):
            print "WARNING: setting a non-list value:"
            print 'Setting %s to %s' % (name,`value`)
            raise ValueError, "Non-list value provided for storage: " + `value`
        elif len(value)>10:
            print 'Setting %s to list' % name
        else:
            print 'Setting %s to %s' % (name,str(value))
        end_value = value
        if not isinstance(value,list):
            print 'Creating list at top level'
            end_value = [a for a in value]
        super(GenericInput,self).__setitem__(name,end_value)

    def has_key(self,name):
        import traceback
        print 'Debug: checking for %s' % name
        try:
            test = self.__getitem__(name,use_drel=False)
        except KeyError:
            print '%s not found (KeyError)' % name
            return False
        if test is None:
            print '%s not found (None returned)' % name
            return False
        return True

    def get_type(self,name):
        """Return the dictionary-defined type of the given canonical name"""
        drel_name = self.get_drel_name(name)
        return self.dictionary[drel_name]['_type.contents']

    def get_drel_name(self,name):
        """Return a value using the canonical name as input"""
        drel_name = [k[0] for k in self.generic_name_table.items() if k[1]==name]
        if len(drel_name)!= 1:
            raise KeyError, 'Unrecognised/ambiguous canonical name %s' % name
        return drel_name[0]
        
    def get_by_canonical_name(self,name):
        drel_name = self.get_drel_name(name)
        return self[drel_name]


# Handling multiple data units
# ----------------------------
# 
# If (as is likely) the output data unit expects only a single value for certain datanames,
# we must emit multiple data units for each value that we encounter.  We create a list of
# multi-valued input datanames, and create a data unit schedule such that each distinct
# combination of values is given a separate data unit. ::

    def slice_and_dice(self,data_unit_spec):
        """Determine which values will need separate data units"""
        multi_vals = {}
        for can_name in data_unit_spec:    #single-valued
            can_vals = self.get_by_canonical_name(can_name)
            if can_vals is not None and len(can_vals)>=1:
                multi_vals[can_name] = set(can_vals)  #unique values
        # create a schedule: an array of values taken by each dataname
        schedule = {}
        for one_name in multi_vals.keys():
            if len(schedule)==0: old_length = 1
            else: old_length = len(schedule[schedule.keys()[0]])
            for one_entry in schedule.keys():
                schedule[one_entry] = schedule[one_entry]*len(multi_vals[one_name])
            schedule[one_name] = []
            [schedule[one_name].extend([p]*old_length) for p in multi_vals[one_name]]
        return schedule


# Figuring out which names should not be array-valued
# ---------------------------------------------------
# 
# We take responsibility for supplying the format adapter with a singleton-list-valued item when
# we have sliced and diced.  We need to check for linked items as well. So we find out the
# category key(s), and see where they are linked to. A key is only single-valued if the key
# that it points to is single-valued, or the key itself is specified as single-valued.  ::

    def find_singleton(self,single_names,one_name):
        """Using dictionary, return True if one_name must not be multi-valued if items in
        single_names are single-valued.  Expects canonical names throughout"""
        drel_single_names = [self.get_drel_name(n) for n in single_names]
        drel_query_name = self.get_drel_name(one_name)
        cat_for_name = self.dictionary[drel_query_name]['_name.category_id']
        keys_for_cat = set(tuple(self.dictionary[cat_for_name].get('_category_key.name',[])))
        down_linked_items = set([self.dictionary[n]['_definition_id'] for n in self.dictionary.keys() if self.dictionary[n].get('_name.linked_item_id','') in drel_single_names])
        all_key_names = set(drel_single_names) | down_linked_items
        print 'Debug: keys for %s ' % one_name
        print `keys_for_cat`
        print 'Single-valued keys:' + `all_key_names`
        must_be_single =  keys_for_cat <= set(all_key_names)
        return must_be_single

# Filters
# -------
# 
# The other side of the coin to slicing and dicing is ensuring that all manipulations
# are performed 'as if' the relevant datanames only take a single value.  We therefore
# define simple 'filters' that are checked each time data are returned to make sure
# that no non-matching rows are provided.  We expect to operate only on keys (or
# pointers to keys) as all items are ultimately functions of keys and therefore keys
# must be present in the file in order to properly interpret any of these datanames
# (i.e. functions of keys). Note all filter names are drel names, not canonical names. ::

    def add_filter(self,item_name,item_value):
        """Allow only rows with item_name == item_value to be returned, including
        any linked keys"""
        drel_name = self.get_drel_name(item_name)
        self.filters[drel_name] = item_value
        linked_items = [k for k in self.dictionary.keys() if self.dictionary[k].get('_name.linked_item_id',None) == drel_name]
        while self.dictionary[drel_name].get('_name.linked_item_id',None) is not None:
            drel_name = self.dictionary[drel_name]['_name.linked_item_id']
            linked_items.append(drel_name)
        for li in linked_items:
            self.filters[li] = item_value
        print 'Linked to %s: ' % item_name 
        print `linked_items`

    def apply_filters(self,name,result):
        """Check all of our filters to see if any match. If so, edit result so
        that only matching entries are returned"""
        if result is None: return result
        drel_name = self.get_drel_name(name)
        drel_cat = self.dictionary[drel_name]['_name.category_id']
        names_in_cat = [n for n in self.dictionary.keys() if self.dictionary[n].get('_name.category_id',"") == drel_cat]
        intersection = [(self.generic_name_table[n],
                         self.dictionary[n]['_type.contents'],
                         self.dictionary[n].get('_units.code',None))\
                        for n in names_in_cat if n in self.generic_name_table.keys() and n in self.filters.keys()]
        print 'Intersection: ' + `intersection`
        actually_there = [n[0] for n in intersection if self.input_module.get_by_name(n[0],n[1],n[2]) is not None]
        # now edit
        print 'Actually there:' + `actually_there`
        accept_list = [True] * len(result)
        for filter_name in actually_there:
            filter_drel = self.get_drel_name(filter_name)
            filter_type = self.dictionary[filter_drel]['_type.contents']
            filter_units = self.dictionary[filter_drel].get('_units.code',None)
            filter_values = self.input_module.get_by_name(filter_name,filter_type,filter_units)
            print 'Ready to filter: %s %s, matching %s' % (filter_name,`filter_values`,`self.filters[filter_drel]`)
            accept_list = [(p[0] and (p[1] in self.filters[filter_drel])) for p in zip(accept_list,filter_values)]
        print 'Filtered on %s, obtained %s for %s' % (actually_there,accept_list,result)
        return [r[0] for r in zip(result,accept_list) if r[1]]
        
# Name translation
# ----------------
# 
# Note that dREL and our dictionary uses names in "_domain.name"
# format, meaning that our "__getitem__" method must convert these names
# into our 'generic' names before accessing the underlying format
# adapter.  Of course, for CIF, we are doing an extra round of
# processing, but we allow this in order to show how a completely
# generic system works. The following table converts a dREL(i.e CIF)
# name to the generic equivalent. ::

    def setup_translation(self):
        """Install a name translation dictionary"""
        self.generic_name_table = {
        "_diffrn_radiation_wavelength.wavelength":"incident wavelength",
        "_diffrn_radiation_wavelength.id":"wavelength id",
        "_diffrn_scan.date_start":"start time",
        "_diffrn_source.current":"source current",
        "_detector_axis_uncoupled_local.id":"simple detector axis id",
        "_detector_axis_uncoupled_local.vector":"simple detector axis vector",
        "_detector_axis_uncoupled_local.offset":"simple detector axis offset",
        "_detector_axis_uncoupled_local.vector_convention2_local":"simple detector axis vector mcstas",
        "_detector_axis_uncoupled_local.offset_convention2_local":"simple detector axis offset mcstas",
        "_detector_axis_uncoupled_local.type":"simple detector axis type",
        "_detector_axis_uncoupled_local.key":"simple detector axis key",
        "_array_structure_list.id":"unique array direction identifier",
        "_array_structure_list.array_id":"array structure array identifier",
        "_array_structure_list.axis_set_id":"array structure axis set",
        "_array_structure_list.index":"array structure index",
        "_array_structure_list.precedence":"array axis set precedence",
        "_array_structure_list_axis.axis_set_id":"detector axis set id",
        "_array_structure_list_axis.axis_id":"detector axis set component axis",
        "_array_structure_list.coupling_number_local":"number of coupled axes",
        "_axis.id":"axis id",
        "_axis.key":"axis key",
        "_axis.vector":"axis vector",
        "_axis.offset":"axis offset",
        "_axis.offset_convention2_local":"axis offset mcstas",
        "_axis.vector_convention2_local":"axis vector mcstas",
        "_axis.type":"axis type",
        "_axis.equipment":"axis equipment",
        "_axis.depends_on":"axis depends on",
        "_axis.vector[1]":"axis vector X component",
        "_axis.vector[2]":"axis vector Y component",
        "_axis.vector[3]":"axis vector Z component",
        "_axis.offset[1]":"axis offset X component",
        "_axis.offset[2]":"axis offset Y component",
        "_axis.offset[3]":"axis offset Z component",
        "_goniometer_axis_local.id":"goniometer axis id",
        "_goniometer_axis_local.key":"goniometer axis key",
        "_goniometer_axis_local.vector":"goniometer axis vector",
        "_goniometer_axis_local.offset":"goniometer axis offset",
        "_goniometer_axis_local.equipment":"goniometer axis equipment",
        "_goniometer_axis_local.offset_convention2_local":"goniometer axis offset mcstas",
        "_goniometer_axis_local.vector_convention2_local":"goniometer axis vector mcstas",
        "_goniometer_axis_local.type":"_goniometer axis type",
        "_goniometer_axis_local.depends_on":"goniometer axis depends on",
        "_goniometer_axis_local.vector[1]":"goniometer axis vector X component",
        "_goniometer_axis_local.vector[2]":"goniometer axis vector Y component",
        "_goniometer_axis_local.vector[3]":"goniometer axis vector Z component",
        "_goniometer_axis_local.offset[1]":"goniometer axis offset X component",
        "_goniometer_axis_local.offset[2]":"goniometer axis offset Y component",
        "_goniometer_axis_local.offset[3]":"detector axis offset Z component",
        "_detector_axis_local.id":"detector axis id",
        "_detector_axis_local.key":"detector axis full id",
        "_detector_axis_local.vector":"detector axis vector",
        "_detector_axis_local.offset":"detector axis offset",
        "_detector_axis_local.offset_convention2_local":"detector axis offset mcstas",
        "_detector_axis_local.vector_convention2_local":"detector axis vector mcstas",
        "_detector_axis_local.type":"_detector axis type",
        "_detector_axis_local.depends_on":"detector axis depends on",
        "_detector_axis_local.vector[1]":"detector axis vector X component",
        "_detector_axis_local.vector[2]":"detector axis vector Y component",
        "_detector_axis_local.vector[3]":"detector axis vector Z component",
        "_detector_axis_local.offset[1]":"detector axis offset X component",
        "_detector_axis_local.offset[2]":"detector axis offset Y component",
        "_detector_axis_local.offset[3]":"detector axis offset Z component",
        "_detector_axis_local.coupled":"detector axis is coupled",
        #"_scan_array_data.array_data":"full simple data",
        #"_scan_array_data.scan_id":"full simple data scan id",
        "_diffrn_scan.id":"scan id",
        "_diffrn_scan.frames":"number of frames",
        "_diffrn_scan.number_of_scanned_axes_local":"number of scanned axes",
        "_diffrn_scan_simple_local.scan_id":"simple scan data id",
        "_diffrn_scan_simple_local.axis_id":"simple scan axis",
        "_diffrn_scan_simple_frames_local.frame_id":"simple scan frame frame id",
        "_diffrn_scan_simple_frames_local.scan_id":"simple scan frame scan id",
        "_diffrn_scan_simple_frames_local.id":"simple scan frame unique identifier",
        "_diffrn_scan_simple_frames_local.array_data":"simple scan data",
        "_diffrn_scan_simple_frames_local.array_id":"simple scan frame array id",
        "_diffrn_scan_simple_frames_local.binary_id":"simple scan data binary id",
        "_diffrn_scan_axis.key":"scan axis key",
        "_diffrn_scan_axis.axis_id":"scan axis axis id",
        "_diffrn_scan_axis.scan_id":"scan axis scan id",
        "_diffrn_scan_axis.angle_increment":"scan axis angle increment",
        "_diffrn_scan_axis.displacement_increment":"scan axis displacement increment",
        "_full_frame_local.id":"full frame id",
        "_full_frame_local.frame_id":"full frame frame id",
        "_full_frame_local.binary_id":"full frame binary id",
        "_full_frame_local.array_id":"full frame array id",
        "_full_frame_local.scan_id":"full frame scan id",
        "_full_frame_local.detector_element_id":"full frame detector element id",
        "_full_frame_local.detector_id":"full frame detector id",
        "_diffrn_detector.key":"detector key",
        "_diffrn_detector.id":"detector id",
        "_diffrn_detector.number_of_axes":"detector number of axes",
        "_diffrn_detector.diffrn_id":"detector scan",
        "_diffrn_detector.detector":"detector name",
        "_diffrn_detector_element.detector_id":"detector element detector id",
        "_diffrn_detector_element.id":"detector element id",
        "_diffrn_detector_element.key":"detector element unique identifier",
        "_diffrn_detector_monolithic_element_local.key":"monolithic detector element unique identifier",
        "_diffrn_detector_monolithic_local.id":"monolithic detector id",
        "_diffrn_detector.number_of_elements_local":"number of detector elements",
        "_diffrn_data_frame.id":"data frame id",
        "_diffrn_data_frame.key":"data frame unique identifier",
        "_diffrn_data_frame.binary_id":"data frame binary id",
        "_diffrn_data_frame.array_id":"data frame array id",
        "_diffrn_data_frame.scan_id":"data frame scan id",
        "_diffrn_data_frame.detector_element_id":"data frame element id",
        "_diffrn_data_frame.detector_element_key":"data frame detector element key",
        "_diffrn_data_frame.detector_id":"data frame detector id",
        "_diffrn_scan_frame.key":"scan frame key",
        "_diffrn_scan_frame.scan_id":"scan frame scan id",
        "_diffrn_scan_frame.frame_id":"scan frame frame id",
        "_diffrn_scan_frame.frame_number":"scan frame sequence number",
        "_diffrn_scan_frame_axis.axis_id":"frame axis location axis id",
        "_diffrn_scan_frame_axis.frame_id":"frame axis location frame id",
        "_diffrn_scan_frame_axis.scan_id":"frame axis location scan id",
        "_diffrn_scan_frame_axis.angle":"frame axis location angular position",
        "_diffrn_scan_frame_axis.displacement":"frame axis location translation",
        "_array_data.binary_id":"2D data identifier",
        "_array_data.array_id":"2D data structure id",
        "_array_data.as_integers_local":"2D data",
        "_simple_data_axis_local.id":"data axis id",
        "_simple_data_axis_local.precedence":"data axis precedence",
        "_simple_data_axis_local.scan_id":"data axis scan id",
        }

# Semantic packets
# ----------------
# 
# See the section on the Packet class to explain why these are important
# in dREL.  DDLm dictionaries allow categories to be nested, which is
# another way of saying that the set of datanames mapping from a single
# domain are split into two or more groups, which as a result have
# different keys that really refer to the same domain.  To account for
# this, we have to loop over the possible keys rather than just do a
# straighforward lookup. ::
 
    def GetKeyedSemanticPacket(self,keyvalue,cat_id):
        """Return a packet containing the values for datanames
        corresponding to the value given for dataname keyname"""
        target_keys = self.dictionary.cat_key_table[cat_id]
        p = Packet(self.dictionary,self)
        # set case-sensitivity flag
        lcase = False
        if self.dictionary[target_keys[0]]['_type.contents'] in ['Code','Tag','Name']:
            lcase = True
        for cat_key in target_keys:
            all_names = [n for n in self.dictionary.keys() if self.dictionary[n].get('_name.category_id',None)==cat_id]
            if not self.has_key(cat_key):
                dummy = self[cat_key]   #try to generate it
                if not self.has_key(cat_key):
                    print 'Warning: key %s not found or generable' % cat_key
                    continue   #couldn't be generated
            try:
                extra_packet = self.GetKeyedPacket(cat_key,keyvalue,all_names,no_case=lcase)
            except ValueError:      #none/more than one, assume none
                continue
            p.merge_packet(extra_packet)
        # the following attributes used to calculate missing values
        for keyname in target_keys:
            if hasattr(p,keyname):
                p.key = keyname
                break
        if not hasattr(p,"key"):
            raise ValueError, "No key found for %s, packet is %s" % (cat_id,str(p))
        return p

    def GetKeyedPacket(self,keyname,keyvalue,all_names,no_case='ignored'):
        """Return a packet that provides the corresponding values of [[all_names]] where
        keyname == keyvalue"""
        key_vals = self[keyname]
        key_pos = list(self[keyname]).index(keyvalue)
        out_packet = Packet(self.dictionary,self)
        for one_name in all_names:
            if self.has_key(one_name):
                print 'Picking element %d of value %s for %s' % (key_pos,`self[one_name]`,one_name)
                target_val = self[one_name][key_pos]
                out_packet.append(target_val)
                setattr(out_packet,one_name,target_val)
        return out_packet

# Unused stubs
# ============
# 
# These stubs are purely to satisfy the requirements of the dictionary derive_item
# method, and are not necessary for correct operation. ::

    def AddLoopName(self,dummy1,dummy2):
        pass

    def CreateLoop(self,key):
        pass

    def ChangeItemOrder(self,key,order):
        pass


# Packets
# =======
# 
# A critical feature of dREL is the ability to index into a different domain and access
# datanames of that domain.  To support this, we have to return a packet which supports
# the 'getattr' method.  The following code is adapted from that found in PyCIFRW. Note
# that in order to further calculate dataname values using the dictionary, each packet 
# stores a link to the full dictionary and the data object. The dictionary object
# has to be set when the packet is created. ::

class Packet(list):
    def __init__(self,dictionary,data_source,*args,**kwargs):
        super(Packet,self).__init__(*args,**kwargs)
        self.cif_dictionary = dictionary
        self.fulldata = data_source

    def merge_packet(self,incoming):
        """Merge contents of incoming packet with this packet"""
        new_attrs = [a for a in dir(incoming) if a[0] == '_' and a[1] != "_"]
        self.extend(incoming)
        for na in new_attrs:
            setattr(self,na,getattr(incoming,na))

    def __getattr__(self,att_name):
        """Derive or obtain a packet attribute"""
        if att_name in self.__dict__:
            return getattr(self,att_name)
        if att_name in ('cif_dictionary','fulldata','key'):
            raise AttributeError, 'Programming error: can only assign value of %s' % att_name
        d = self.cif_dictionary
        c = self.fulldata
        k = self.key
        if not c.has_key(att_name):
            print "===Deriving item %s for packet" % att_name
            try:
                result = d.derive_item(att_name,c,store_value=True,allow_defaults=False)
            except StarFile.StarDerivationError:
                result = None
            if result is None:   #try with defaults
                d.derive_item(att_name,c,store_value=True,allow_defaults=True)
            print "===Finished packet derivation for %s" % att_name
        # 
        # now pick out the new value
        keyval = getattr(self,k)
        cat_id = self.cif_dictionary[k]['_name.category_id']
        all_names = [n for n in self.cif_dictionary.keys() if self.cif_dictionary[n].get('_name.category_id',None) == cat_id]
        full_pack = c.GetKeyedPacket(k,keyval,all_names)
        return getattr(full_pack,att_name)

# Overall control
# ===============
# 
# This class is responsible for overall control of the transformation. ::

class TransformManager(object):
    """Manage datafile transformation"""
    def __init__(self):
        self.plugin_list = {}

    def register(self,adapter_class,mnemonic):
        self.plugin_list[mnemonic] = adapter_class
        # we could check API conformance here
        
    def set_dictionary(self,dic):
        """Set the DDLm dictionary for use with this class"""
        self.def_dic = CifDic(dic,grammar="2.0")
        
    def manage_transform(self,out_bundle,infile,intype,outfile,outtype,unit_name=None):
        """Manage a file type transformation"""
        all_names = out_bundle[:]
        in_module = self.plugin_list[intype]
        out_module = self.plugin_list[outtype]
        in_handle = in_module.open_file(infile)
        in_unit = in_module.open_data_unit(entryname=unit_name)
        generic = GenericInput(in_module,self.def_dic)
        data_unit_spec = out_module.get_single_names()   #defines data unit
        # leave in datanames that are potentially multi-valued
        drel_names = [generic.get_drel_name(n) for n in data_unit_spec]
        name_cats = [self.def_dic[n]['_name.category_id'] for n in drel_names]
        cat_type = [self.def_dic[n].get('_definition.class','Datum') for n in name_cats]
        were_multi = [n[0] for n in zip(data_unit_spec,cat_type) if n[1] == 'Loop'] 
        print 'Following names single valued on output: ' + `were_multi`
        output_schedule = generic.slice_and_dice(were_multi)
        print 'Generated data entry output schedule: ' + `output_schedule`
        def write_out_names(single_valued_names):
            """Output names, with those that are not listed provided in the argument"""
            for name in all_names:
                result = generic.get_by_canonical_name(name)
                if result is None:
                    print "Skipping %s, not found or derivable from input file" % name   # can't be done
                else:#now output this value
                #    if name in single_valued_names:
                #        result = result[0]   #remove one level of listing
                    out_module.set_by_name(name,result,generic.get_type(name))

        if len(output_schedule)>0:
            [all_names.remove(n) for n in were_multi if n in output_schedule.keys() and n in all_names]  #remove unneeded names
            must_be_single = [n for n in all_names if generic.find_singleton(output_schedule.keys(),n)]
            print 'Single-valued: ' + `must_be_single`
            for single_data_unit in range(len(output_schedule[output_schedule.keys()[0]])):
                print 'Creating data unit for value %s' % output_schedule[output_schedule.keys()[0]]
                out_unit = out_module.create_data_unit()
                filter_names = output_schedule.keys()
                [generic.add_filter(k,output_schedule[k]) for k in filter_names]
                for unit_key in output_schedule:
                    out_module.set_by_name(unit_key,generic.get_by_canonical_name(unit_key),generic.get_type(unit_key))
                    # out_module.set_by_name(unit_key,output_schedule[unit_key][single_data_unit],
                    #                           generic.get_type(unit_key))
                write_out_names(must_be_single)
                out_module.close_data_unit()
        else:
            out_module.create_data_unit()
            write_out_names([])
            out_module.close_data_unit()

        out_module.output_file(outfile)        
    
