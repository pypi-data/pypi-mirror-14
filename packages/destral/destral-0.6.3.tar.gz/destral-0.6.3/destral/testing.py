import logging
import unittest

from destral.openerp import OpenERPService
from destral.transaction import Transaction
from osconf import config_from_environment


logger = logging.getLogger('destral.testing')


class OOTestCase(unittest.TestCase):
    """Base class to inherit test cases from for OpenERP Testing Framework.
    """

    require_demo_data = False

    @property
    def database(self):
        """Database used in the test.
        """
        return self.openerp.db_name

    @classmethod
    def setUpClass(cls):
        """Set up the test

        * Sets the config using environment variables prefixed with `DESTRAL_`.
        * Creates a new OpenERP service.
        * Installs the module to test if a database is not defined.
        """
        cls.config = config_from_environment(
            'DESTRAL', ['module'], use_template=True
        )
        ooconfig = {}
        if cls.require_demo_data:
            cls.config['use_template'] = False
            ooconfig['demo'] = {'all': 1}
        cls.openerp = OpenERPService(**ooconfig)
        cls.drop_database = False
        if not cls.openerp.db_name:
            cls.openerp.db_name = cls.openerp.create_database(
                cls.config['use_template']
            )
            cls.drop_database = True
            cls.install_module()

    @classmethod
    def install_module(cls):
        """Install the module to test.
        """
        cls.openerp.install_module(cls.config['module'])

    def test_all_views(self):
        """Tests all views defined in the module.
        """
        logger.info('Testing views for module %s', self.config['module'])
        imd_obj = self.openerp.pool.get('ir.model.data')
        view_obj = self.openerp.pool.get('ir.ui.view')
        with Transaction().start(self.database) as txn:
            imd_ids = imd_obj.search(txn.cursor, txn.user, [
                ('model', '=', 'ir.ui.view'),
                ('module', '=', self.config['module'])
            ])
            if imd_ids:
                views = {}
                for imd in imd_obj.read(txn.cursor, txn.user, imd_ids):
                    view_xml_name = '{}.{}'.format(imd['module'], imd['name'])
                    views[imd['res_id']] = view_xml_name
                view_ids = views.keys()
                logger.info('Testing %s views...', len(view_ids))
                for view in view_obj.browse(txn.cursor, txn.user, view_ids):
                    view_xml_name = views[view.id]
                    model = self.openerp.pool.get(view.model)
                    if model is None:
                        # Check if model exists
                        raise Exception(
                            'View (xml id: %s) references model %s which does '
                            'not exist' % (view_xml_name, view.model)
                        )
                    logger.info('Testing view %s (id: %s)', view.name, view.id)
                    model.fields_view_get(txn.cursor, txn.user, view.id,
                                          view.type)
                    if view.inherit_id:
                        while view.inherit_id:
                            view = view.inherit_id
                        model.fields_view_get(txn.cursor, txn.user, view.id,
                                              view.type)
                        logger.info('Testing main view %s (id: %s)',
                                    view.name, view.id)

    @classmethod
    def tearDownClass(cls):
        """Tear down the test.

        If database is not defined, the database created for the test is
        deleted
        """
        if cls.drop_database:
            cls.openerp.drop_database()
            cls.openerp.db_name = False
