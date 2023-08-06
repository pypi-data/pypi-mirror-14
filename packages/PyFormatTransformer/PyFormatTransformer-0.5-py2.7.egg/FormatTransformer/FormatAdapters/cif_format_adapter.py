# Introduction
# ============
# 
# This is a demonstration format adapter for CIF as described by Hester (2016).
# Format adapters set and return data in a uniform (domain,name) presentation.  All
# format adapter collections must agree on how values and units are to be
# presented. Here we choose Numpy representation, and standard units of
# 'metres' for length.  This adapter is not intended to be
# comprehensive, but instead to show how a full adapter might be
# written.
# 
# Three routines are required:
# 1. get_by_name(name,type,domain=None)
# Return a numpy array or string corresponding to
# all values associated with name. Type
# is restricted to "real", "text" or "int".
# 2. set_by_name(domain,name,values,type)
# Set all values for (domain,name)
# 3. set_by_domain_value(domain,domain_value,name,value,type)
# Set the value of name corresponding to the value of domain equalling (domain,name)
# 
# We use the pycifrw library for access, and the pycbf library for image
# handling.  Because pycbf requires initialising from the filename, but
# is called from within a pycifrw CifBlock structure, we have to carry
# along our file location and blockname in our data object, which we
# simply do using the magic of Python dynamic assignment. ::

import numpy
from CifFile import CifFile, CifBlock
convert_probe = 'dummy'  #forward definition

# Configuration data
# ==================
# 
# These tables show which datanames are grouped together, and how canonical names match up to 
# CIF names.  Canonical names are either
# a direct match, or individual values are embedded in a string value.  None of
# the latter are covered here. An optional function is included in case the
# value has to be converted (units, list of restricted values, array creation). CIF files can
# contain single-dataname keys, or combinations of datanames which form a compound key.
# We express this situation by giving the key as a (single-key,(compound_key_1,compound_key_2...))
# tuple. ::


canonical_groupings = {('wavelength id',()):['incident wavelength'],
('axis id',()):['axis vector','axis offset','axis type'],
('2D data identifier',()):['2D data'],
('frame axis location key',('frame axis location axis id','frame axis location scan id',
                            'frame axis location frame id')):['frame axis location angular position'],
('data frame key',('data frame scan id','data frame id')):['data frame binary id',
                                                           'data frame element id',
                                                           'data frame detector id',
                                                           'data frame detector element key',
                                                           'data frame array id']
}

canonical_name_locations = {
"source current": ["_diffrn_source.current",None],
"incident wavelength":["_diffrn_radiation_wavelength.wavelength",None],
"wavelength id":["_diffrn_radiation_wavelength.id",None],
"probe":["_diffrn_radiation.probe",convert_probe],
"start time": ["_diffrn_scan.date_start",None],
"axis vector":["_axis.vector",None],
"axis offset":["_axis.offset",None],
"axis type":["_axis.type",None],
"axis id":["_axis.id",None],
"axis equipment":["_axis.equipment",None],
"detector axis set id":["_array_structure_list_axis.axis_set_id",None],
"detector axis set component axis":["_array_structure_list_axis.axis_id",None],
"axis vector X component":["_axis.vector[1]",None],
"axis vector Y component":["_axis.vector[2]",None],
"axis vector Z component":["_axis.vector[3]",None],
"axis offset X component":["_axis.offset[1]",None],
"axis offset Y component":["_axis.offset[2]",None],
"axis offset Z component":["_axis.offset[3]",None],
"scan id":["_diffrn_scan.id",None],
"number of frames":["_diffrn_scan.frames",None],
"scan axis key":["_diffrn_scan_axis.key",None],
"scan axis axis id":["_diffrn_scan_axis.axis_id",None],
"scan axis scan id":["_diffrn_scan_axis.scan_id",None],
"scan axis angle increment":["_diffrn_scan_axis.angle_increment",None],
"scan axis displacement increment":["_diffrn_scan_axis.displacement_increment",None],
"detector key":["_diffrn_detector.key",None],
"detector id":["_diffrn_detector.id",None],
"detector number of axes":["_diffrn_detector.number_of_axes",None],
"detector scan":["_diffrn_detector.diffrn_id",None],
"detector name":["_diffrn_detector.detector",None],
"detector element detector id":["_diffrn_detector_element.detector_id",None],
"detector element id":["_diffrn_detector_element.id",None],
"data frame id":["_diffrn_data_frame.id",None],
"data frame binary id":["_diffrn_data_frame.binary_id",None],
"data frame array id":["_diffrn_data_frame.array_id",None],
"data frame scan id":["_diffrn_data_frame.scan_id",None],
"data frame element id":["_diffrn_data_frame.detector_element_id",None],
"data frame detector id":["_diffrn_data_frame.detector_id",None],
"data frame detector element key":['_diffrn_data_frame.detector_element_key',None],
"data frame key":["_diffrn_data_frame.key",None],
"scan frame key":["_diffrn_scan_frame.key",None],
"scan frame scan id":["_diffrn_scan_frame.scan_id",None],
"scan frame frame id":["_diffrn_scan_frame.frame_id",None],
"scan frame sequence number":["_diffrn_scan_frame.frame_number",None],
"frame axis location axis id":["_diffrn_scan_frame_axis.axis_id",None],
"frame axis location axis displacement":["_diffrn_scan_frame_axis.displacement",None],
"frame axis location angular position":["_diffrn_scan_frame_axis.angle",None],
"frame axis location frame id":["_diffrn_scan_frame_axis.frame_id",None],
"frame axis location key":["_diffrn_scan_frame_axis.key",None],
"frame axis location scan id":["_diffrn_scan_frame_axis.scan_id",None],
"simple scan frame key":["_diffrn_scan_simple_frame.key",None],
"2D data identifier":["_array_data.binary_id",None],
"2D data structure id":["_array_data.array_id",None],
"2D data":["_array_data.as_integers_local",None],
"array structure array identifier":["_array_structure_list.array_id",None],
"unique array direction identifier":["_array_structure_list.id",None],
"array axis set precedence":["_array_structure_list.precedence",None],
"array structure index":["_array_structure_list.index",None],
"array structure axis set":["_array_structure_list.axis_set_id",None],
"detector axis set id":["_array_structure_list_axis.axis_set_id",None],
"detector axis set component axis":["_array_structure_list_axis.axis_id",None]
}

# The adapter class
# =================
# 
# In general PyCIFRW provides us with adequate support, but for uniformity we
# use the same structure as the NeXus adapter. ::

class CifAdapter(object):
    """A class to implement a uniform format adapter for CIF"""
    def __init__(self,location_config,domain_config):
        self.name_locations = location_config
        self.domain_names = domain_config
        self.filehandle = None
        self.cifblock = None
        self.all_blocks = []

# Converting values
# =================
# 
# We start out matching the types 'Real', 'Int' and 'Text'.  As CIF is text-based,
# this means we simply apply the relevant conversions.  For speed, we assume
# that incoming is iterable, rather than mapping [[convert_type]] itself to
# each element. Note also that the interchange datatype is a numpy array. ::

    def convert_type(self,incoming,target_type):
        """Convert all elements of incoming to [[target_type]]"""
        if not isinstance(incoming,(list,tuple)):
            incoming = [incoming]
        if target_type == "Real":
            final_type = numpy.require(incoming,'float')
        elif target_type in ("Count","Index","Integer"):
            final_type = numpy.require(incoming,'int')
        elif target_type in ("Text","Code"):
            final_type = numpy.atleast_1d(incoming)
        else:
            raise ValueError, 'Type %s not recognised' % target_type
        return final_type

# Converting simple lists
# -----------------------
# 
# Some values are chosen from short lists of alternatives.  The following routine
# lists the conversions. ::

    def convert_probe(incoming):
        """Convert the value of incoming to the appropriate one for
        radiation type"""
        # not yet done.
        return incoming

# The API functions
# =================
# 
# Obtaining values
# ----------------
# 
# We very simply return the specified dataname, unless an image is requested, in 
# which case we have to process the CBF/imgCIF image data into a standard,
# format agnostic numpy array.  We cache this to avoid reading a multi-megabyte
# file every time. ::

    def get_by_name(self,name,value_type,units=None):
        """Return values as [[value_type]] for [[name]]"""
        if name == "2D data":  #special name
            if self.cifblock.image_cache is None:
                print "CIF: creating image cache"
                all_images = self.create_images()
                self.cifblock.image_cache = all_images
            print 'CIF: Returning contents of image cache'
            return self.cifblock.image_cache
        else:
            cif_location,transform = self.name_locations.get(name,(None,None))
            if cif_location is None:
                print "CIF: no location found for %s" % name
                return None
            try:
                values = self.cifblock[cif_location]
            except KeyError:
                print "Couldn't find %s" % cif_location
                return None    #couldn't be done
            if transform is not None:
                values = transform(values)
            if isinstance(values,(basestring,int,float,complex)):
                values = [values]
            return self.convert_type(values,value_type)

# Setting values
# --------------
# 
# CIF requires everything to be a string.  This is handled automatically
# by the PyCIFRW system, and the supplied value is assumed to be correct.
# We store the images until the block is finished in order to provide 
# the binary id to the image encoding routine, which encodes it in
# the header. ::

    def set_by_name(self,name,value,value_type,units=None):
        import numpy
        if name == "2D data": 
            self.output_image_cache = map(numpy.array,value)
            return
        cif_location = self.name_locations.get(name,(None,None))[0]
        if cif_location is not None:
            self.cifblock[cif_location] = value


# Housekeeping
# ------------
# 
# When opening and closing files and data units, we record the filename and
# blockname so that we can reopen the file with pycbf if asked for an image. ::

    def open_file(self,filename):
         """Open the CIF file [[filename]], returning a handle"""
         self.filehandle = CifFile(filename,grammar="auto")

    def open_data_unit(self,entryname=None):
        """Open a particular datablock. If
        an entryname is not provided, a quasi-random one is
        returned"""
        if entryname is not None and self.filehandle.has_key(entryname):
            self.cifblock = self.filehandle[entryname]
            self.cifblock.blockname = entryname  #remember
        elif entryname is None:
            self.cifblock = self.filehandle.first_block()
            self.cifblock.blockname = self.filehandle.keys()[0]
        else:
            raise KeyError, 'No such block %s in CIF file' % entryname
        self.cifblock.filename = self.filehandle.my_uri
        self.cifblock.image_cache = None

    def create_data_unit(self,entryname = None):
        """Start a new data unit"""
        self.cifblock = CifBlock()
        self.output_image_cache = None
        if entryname is not None:
            self.cifblock.blockname = entryname

# The following truncates binary_id as pycbf expects relatively short integers for
# binary_id. ::

    def close_data_unit(self):
        """Finish off [[datablock]] in file [[datafile]]"""
        # create any necessary encoded images
        if self.output_image_cache is not None:
            binary_ids = [int(a) for a in self.cifblock['_array_data.binary_id']]
            self.cifblock['_array_data.data'] = [apply(self.encode_images,a) for a in zip(self.output_image_cache,binary_ids)]
            all_ids = ['_array_data.'+ n for n in ['binary_id','array_id','data']]
            loop_ids = [a for a in all_ids if self.cifblock.has_key(a)]
            self.cifblock.CreateLoop(loop_ids)
        # create the loops

# We have a choice of outputting the single-dataname key, or else all of the compound keys
# and optionally the single-dataname key. ::

        for key_ids,other_names in self.domain_names.items():
            # key is either
            single_key = key_ids[0]
            single_key = self.name_locations[single_key][0]
            single_key = [s for s in [single_key] if self.cifblock.has_key(s)]
            compound_keys = [self.name_locations[c][0] for c in key_ids[1]]
            compound_keys = [c for c in compound_keys if self.cifblock.has_key(c)]
            true_others = [self.name_locations[o][0] for o in other_names]
            all_names = [t for t in true_others if self.cifblock.has_key(t)]
            print 'CIF: keys, true_others:' + `single_key` + `compound_keys` + `true_others`
            have_keys = len(single_key)==1 or (len(compound_keys)==len(key_ids[1]))
            if len(all_names)>0:
                key_list = []
                if single_key: key_list += single_key
                if have_keys: key_list += compound_keys
                print "CIF: creating loop with " + `key_list+all_names`
                self.cifblock.CreateLoop(key_list+all_names)
        self.all_blocks.append(self.cifblock)
        self.cifblock = None
        self.output_image_cache = None
        return

    def output_file(self,filename):
        """Output a file containing the list of datablocks"""
        cf = CifFile()
        # for each generate simple block name
        for block in self.all_blocks:
            if hasattr(block,"blockname"):
                newblockname = block.blockname
            else:
                newblockname = "Block_%d" % (len(cf)+1)
            cf[newblockname] = block
        f = open(filename,"w")
        f.write(str(cf))
        f.close()

# Single names
# ------------
# 
# We report which datanames must be single-valued: in our case, none. ::

    def get_single_names(self):
       return []

# Creating images
# ===============
# 
# The image data stored in imgCIF is a string (as CIF has not yet
# defined images in terms of CIF2 array types) which require further
# processing to create a multidimensional Numpy array.  The present
# routine returns a proper array for each image in the file.  Note that this
# routine is for demonstration purposes and does not attempt to
# cover all possible array presentations possible in imgCIF: the
# point is that such processing is handled only in this format
# adapter routine and nowhere else. ::

    def create_images(self):
        import pycbf
        """Return a set of numpy image arrays for this file"""
        import numpy
        # for each image, get the array
        blockname = self.cifblock.blockname.encode('ascii','ignore') #plain ASCII
        filename = self.cifblock.filename
        print 'Getting image from file %s, block %s' % (filename,blockname)
        cbf_file = pycbf.cbf_handle_struct()
        cbf_file.read_file(filename,pycbf.MSG_DIGEST)
        cbf_file.rewind_datablock()
        cbf_file.find_datablock(blockname)
        cbf_file.find_category('array_data')
        cbf_file.find_column('data')
        cbf_file.rewind_row()  #start at first row
        no_of_rows = cbf_file.count_rows()
        print 'Found %d rows in %s[%s]' % (no_of_rows,filename,blockname)
        final_images = []
        for image_no in range(no_of_rows):
            parms = cbf_file.get_integerarrayparameters_wdims_fs()
            elsize = parms[2]
            if elsize == 4:
                el_type = numpy.uint32
            elif elsize == 8:
                el_type = numpy.uint64
            dimfast = parms[9]
            dimslow = parms[11]
            dimmid = parms[10]
            print 'Image %d: %d x %d' % (image_no,dimfast,dimmid)
            string_image = cbf_file.get_integerarray_as_string()
            numpy_image = numpy.fromstring(string_image,el_type)
            ff = numpy_image.reshape(dimfast,dimmid)
            final_images.append(ff)
            cbf_file.next_row()
        return final_images

# Storing images
# ==============
# 
# We have to encode the images that we have into strings, and once again use
# pycbf to do the heavy lifting. This routine is called when each image is
# provided. ::

    def encode_images(self,one_image,binary_id):
        import pycbf   #version 0.9.2 tested
        """Convert a 2D image array into a compressed string for storage, using
        binary_id as identifier (binary id should be an integer)."""
        import numpy,cStringIO
        # prepare the data
        a_dims = one_image.shape
        a_size = one_image.size
        as_string = one_image.tobytes()
        # create a temporary file for each image
        cbf_file = pycbf.cbf_handle_struct()
        cbf_file.new_datablock("temp1")
        cbf_file.new_category('array_data')
        cbf_file.new_column('data')
        cbf_file.set_integerarray_wdims(pycbf.CBF_BYTE_OFFSET,
                                  binary_id,as_string,one_image.itemsize,0,a_size,
                                  pycbf.get_local_integer_byte_order(),a_dims[0],a_dims[1],1,0)
        cbf_file.write_file("cbf_scratch.cif",pycbf.CIF,pycbf.HDR_DEFAULT,pycbf.ENC_DEFAULT)
        #now read in the encoded image as a string and return it
        image_enc = CifFile("cbf_scratch.cif").first_block()['_array_data.data']
        return image_enc
        
