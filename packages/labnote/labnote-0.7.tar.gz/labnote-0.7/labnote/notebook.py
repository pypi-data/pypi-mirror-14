"""
Notebook class definition
"""
import fnmatch
import glob
import os
import sys
import time
import yaml
from argparse import ArgumentParser
from collections import OrderedDict
from labnote.categories import CategoryManager
from labnote.entry import Entry
from labnote.renderer import HTMLRenderer

class Notebook(object):
    """Notebook class"""
    def __init__(self, conf=None, **kwargs):
        """Creates a new notebook instance"""
        print("- Starting Labnote")

        print(" LOADING")

        # Get default args
        config = self._load_config(conf, **kwargs)

        # Set object attributes
        self.author = config['author']
        self.email = config['email']
        self.exclude = config['exclude']
        self.title = config['title']
        self.input_dirs = config['input_dirs']
        self.output_file = config['output_file']
        self.include_files = config['include_files']
        self.theme = config['theme']
        self.url_prefix = config['url_prefix']
        self.sort_categories_by_date = config['sort_categories_by_date']

        # Get current date string
        self.date = time.strftime('%Y/%m/%d')

        # Load categories
        self.entries = CategoryManager(config['categories'])
        
        # Find valid notebook entry directories
        self._parse_entries() 


        self._sort_entries()

        # Create a Renderer instance
        self.renderer = HTMLRenderer(self.author, self.title, self.email,
                                     self.date, self.entries, self.output_file,
                                     self.theme)
        print("- Finished")

    def _find_valid_files(self):
        """Search specified locations for files that corresponding to lab
        notebook entries.

        The lab notebook consists of a collection of entries, each
        corresponding to a particular analysis, script, etc. Labnote searches
        the specified input paths for any files matching the allowed file types
        (e.g. *.html, *.py), and adds an entry for each item in the resulting
        notebook. This is the function which scans for acceptable files to
        build entries from, and produces a list of filepaths which can then be
        converted to entry dicts.
        
        Returns
        -------
            A list of filepaths corresponding to items that should form the
            basis of the lab notebook entries.
        """
        filepaths = []

        # Iterate over sub-directories in each search path
        for input_dir in self.input_dirs:
            print("- Scanning for notebook entries in %s" % input_dir)

            for sub_dir in glob.glob(input_dir):
                if not os.path.isdir(sub_dir):
                    continue

                for filename in os.listdir(sub_dir):
                    filepath = os.path.join(sub_dir, filename)
                    if not os.path.isfile(filepath):
                        continue

                    # Skip files which match one of the exclude patterns
                    if any([x in filepath for x in self.exclude]):
                        continue
                
                    # For each file in the top-level of a matching dir, check
                    # to see if it is a valid notebook entry file
                    if any(fnmatch.fnmatch(filename, pattern) for 
                            pattern in self.include_files):
                        filepaths.append(filepath)

        return filepaths

    def _parse_entries(self):
        """Creates notebook entries"""

        # Find files to use for notebook generation
        filepaths = self._find_valid_files()

        # Directory where results will be outputted
        output_dir = os.path.dirname(self.output_file)

        # Iterate over matches files and create notebook entries
        for filepath in filepaths:
            # Check for .labnote file in directory
            metafile = os.path.join(os.path.dirname(filepath), '.labnote')

            kwargs = {}

            if os.path.exists(metafile):
                with open(metafile) as fp:
                    metadata = yaml.load(fp)

                filename = os.path.basename(filepath)
                if filename in metadata.keys():
                    kwargs = metadata[filename]

            # Create a new notebook Entry instance
            entry = Entry.factory(filepath, output_dir, self.url_prefix,
                                  **kwargs)

            # Add entry
            if 'category' in kwargs:
                self.entries.add_entry(entry, kwargs['category'])
            else:
                self.entries.add_entry(entry)


    def _sort_entries(self):
        """Sorts notebook entries"""
        # Sort categories by order of date last modified
        if self.sort_categories_by_date:
            self.entries = CategoryManager(
                sorted(self.entries.items(), 
                       key=lambda x: getattr(x[1][0], 'date'), 
                       reverse=True))

        self.entries.sort_entries()

    def _load_config(self, config_filepath, **kwargs):
        """Loads labnote configuration
       
        This function determines which settings to use when running Labnote.
        Settings may be specified in several different ways. The order to
        precedence is:

        1. Kwargs specified in Notebook constructor
        2. Configuration file specified by `conf` argument to `_load_config`
        3. Command-line options
        4. User configuration (~/.config/labnote/config.yaml)
        5. Defaults

        Args:
            config_filepath: (Optional) Configuration filepath to use.
            kwargs: (Optional) Arguments specified via Notebook constructor.
       
        Returns:
            config: OrderedDict containing labnote settings.
        """
        # Load configuration
        parser = self._get_args()

        # Convert input arguments to a python dict
        args = parser.parse_args()
        args = dict((k, v) for k, v in list(vars(args).items()) if v is not None)

        # Default configuration options
        config = self._get_defaults()

        # If user specified a configuration filepath in the command, use that path
        if 'config' in args:
            if not os.path.isfile(args['config']):
                print("Invalid configuration path specified: %s" % args['config'])
                sys.exit()

            print("- Using configuration: %s" % args['config'])

            # Load config specified from run arguments
            with open(args['config']) as fp:
                config.update(self._ordered_load(fp))
        else:
            # Check for configuration file specified in the Notebook
            # constructor.
            if config_filepath is not None:
                config_file = config_filepath
            else:
                # Otherwise, load user config file if it exists
                config_dir = os.path.expanduser("~/.config/labnote/")

                # Check for config.yaml or config.yml
                config_file = os.path.join(config_dir, 'config.yml')
                if not os.path.isfile(config_file):
                    config_file = os.path.join(config_dir, 'config.yaml')

            # If user config exists, use it to overwrite defaults
            if os.path.isfile(config_file):
                print("- Using configuration: %s" % config_file)
                with open(config_file) as fp:
                    config.update(self._ordered_load(fp))

        # Update default arguments with user-specified settings
        config.update(args)

        # Update with arguments specified to Notebook constructor
        config.update(kwargs)

        # Check for required parameters
        if 'input_dirs' not in config:
            parser.print_help()
            print("Error: missing input directory(s).")
            sys.exit()
        elif 'output_file' not in config:
            parser.print_help()
            print("Error: missing output filepath.")
            sys.exit()

        return config

    def _get_args(self):
        """Parses input and returns arguments"""
        parser = ArgumentParser(description='Generate HTML lab notebook.')

        parser.add_argument('-c', '--config',
                            help=('Configuration filepath. (Will use configuration' 
                                'in $HOME/.config/labnote/config.yml, if it exists.)'))
        parser.add_argument('-i', '--input-dirs', dest='input_dirs', nargs='+',
                            help=('Input directory(s) containing notebook entries.'))
        parser.add_argument('-o', '--output-file', dest='output_file',
                            help=('Location to output notebook HTML to.'))
        parser.add_argument('-u', '--url-prefix', dest='url_prefix',
                            help=('Prefix to add to each entry URL. (Default: "")'))

        return parser

    # Default options
    def _get_defaults(self):
        """Gets a dictionary of default options"""

        return {
            'author': '',
            'entries': {},
            'email':  '',
            'exclude': [],
            'include_files':  ['*.html', '*.py', '*.ipynb'],
            'input_dirs': None,
            'output_file': None,
            'sort_categories_by_date': True,
            'theme': 'default',
            'title': 'Lab Notebook',
            'url_prefix': ''
        }

    def _ordered_load(self, stream, Loader=yaml.Loader,
                     object_pairs_hook=OrderedDict):
        """
        Order-preserving YAML parser

        Creates a python representation of a YAML file in the usual manner,
        except that dictionaries are stored as OrderedDict instances,
        preserving the order in which they appear in the YAML file.

        Source: http://stackoverflow.com/a/21912744/554531

        Args:
            stream: The YAML source stream
            Loader: Base YAML loader class (default: yaml.Loader)
            object_pairs_hook: Class to use for storing dicts. (default:
                OrderedDict)
        Returns:
            An OrderedDict or similar instance representation of the input YAML.
        """

        class OrderedLoader(Loader):
            pass
        def construct_mapping(loader, node):
            loader.flatten_mapping(node)
            return object_pairs_hook(loader.construct_pairs(node))
        OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_mapping)
        return yaml.load(stream, OrderedLoader)

    def render(self):
        """Renders the notebook into HTML"""
        self.renderer.render()

