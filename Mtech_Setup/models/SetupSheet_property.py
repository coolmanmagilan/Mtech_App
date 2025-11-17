from odoo import models, fields, api
import base64
from io import BytesIO
from pdf2image import convert_from_bytes

class SetupSheet_Property(models.Model):
    _name = "master.sheet"
    _description = "Setup Sheet Property"

    Part_id = fields.Many2one("setup.history", string="Part Number")
    SetupSheet_Child = fields.One2many('setup.sheet','SetupSheet_Ref',string='Tools')
    Gallery_id = fields.One2many('setup.gallery','SetupTool_id',string="Gallery")

    EmployeeName = fields.Selection([('prasana','Prasana'),
                                     ('bala', 'Bala'),
                                     ('carl', 'Carl'),
                                     ('kipson', 'Kipson'),
                                     ('daryl', 'Daryl'),
                                     ('mahesh', 'Mahesh'),
                                     ('pretheepan', 'Pretheepan')], string="Technician Name")
    Date = fields.Datetime(string="Date")
    Customers = fields.Many2one('setup.customer',string="Customer")

    def _machineid_list(self):
        selection = []
        for j in range(100):
            a = 'MTL' + "{:03d}".format(j+1)
            selection.append((a, a))

        return selection

    Machine_ID = fields.Selection(string="Machine ID",
                                 selection=lambda self: self._machineid_list())

    DrawingNumber = fields.Char(string="Drawing Number", related='Part_id.DrawingNumber', readonly=False)
    Revision = fields.Char(string="Revision", related='Part_id.Revision', readonly=False)
    Material = fields.Char(string="Material", related = 'Part_id.Material', readonly=False)
    CNC_ProgramNumber = fields.Char(string="CNC Program #", readonly=False)


    def _operation_list(self):
        increment = 10
        selection = []
        for j in range(100//10):
            a = 'OP' + str(increment*(j+1))
            selection.append((a,a))

        return selection

    Operation = fields.Selection(string="Operation",
                                 selection=lambda self:self._operation_list())

    CycleTime = fields.Char(string="Cycle Time", related='Part_id.CycleTime', readonly=False)
    WorkOffset = fields.Char(string="Work Offset", related='Part_id.WorkOffset', readonly=False)
    WorkHolding = fields.Char(string="Work Holding", related='Part_id.WorkHolding', readonly=False)
    MountingFixture = fields.Char(string="Mounting Fixture", related='Part_id.MountingFixture', readonly=False)

    LessonLearntNotes = fields.Text(string="Lesson Learnt", related='Part_id.LessonLearntNotes', readonly=False)
    ProgramModificationNotes = fields.Text(string="Any Porgram Modification?", related='Part_id.ProgramModificationNotes', readonly=False)
    Paths = fields.Binary(string="Path")

    SetupVerified = fields.Char(string="Setup Verified by", related='Part_id.SetupVerified', readonly=False)
    RecordVerified = fields.Char(string="Record Verified by", related='Part_id.RecordVerified', readonly=False)

    ProgramNumber = fields.Char(string="Program Number", related='Part_id.ProgramNumber', readonly=False)
    CustomerPartNumber = fields.Char(string="Customer Part Number", related='Part_id.CustomerPartNumber', readonly=False)
    ECL = fields.Char(string="ECL")

    SafetyEquipment = fields.Char(string="Safety Equipment", related='Part_id.SafetyEquipment', readonly=False)

    DateIssued = fields.Datetime(string="Date Issued", related='Part_id.DateIssued', readonly=False)
    DateRevised = fields.Datetime(string="Date Revised", related='Part_id.DateRevised', readonly=False)

    PartImage = fields.Image(string="Part Image", related='Part_id.PartImage', readonly=False)

    ControllerDocument = fields.Binary(string="Controller Document", related='Part_id.ControllerDocument', readonly=False)
    ControllerDocument_filename = fields.Char(string="Controller Document filename", related='Part_id.ControllerDocument_filename', readonly=False)

    ControllerImage = fields.Image(string="Controller Image",compute="_compute_image_file",store=True)

    @api.depends('ControllerDocument')
    def _compute_image_file(self):
        for record in self:
            if not record.ControllerDocument:
                record.ControllerImage = False
                continue
            pdf_bytes = base64.b64decode(record.ControllerDocument)
            images = convert_from_bytes(pdf_bytes, dpi=300)
            if images:
                img_io = BytesIO()
                images[0].save(img_io, format='PNG')
                img_io.seek(0)
                record.ControllerImage = base64.b64encode(img_io.read())
            else:
                record.ControllerImage = False



    def print_pdf(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.report',
            'name': 'Print Setup Sheet Report',
            'model': 'master.sheet',
            'report_type':'qweb-pdf',
            'report_name':'Mtech_Setup.setup_sheet_report_template',
            'report_file':'Mtech_Setup.setup_sheet_report_template',
            'print_report_name':'Setup Sheet Report',
            'binding_type':'report'
        }



#####################Tool Table#####################################

class SetupTool(models.Model):
    _name = 'setup.sheet'
    _description = 'Setup Tool'

    ###Many2one####
    SetupSheet_Ref = fields.Many2one('master.sheet', string='Setup Sheet')

    Tool_id = fields.Many2one('tool.property', string='Select Tool', readonly=False)


    ToolHolder = fields.Char(string='Tool Holder')
    InsertDescription = fields.Char(string='Insert Description')
    ToolNumber = fields.Char(string='Tool Number', related='Tool_id.ToolNumber')
    ToolDescription = fields.Char(string='Tool Description', related='Tool_id.ToolDescription')

    ImageGallery = fields.Binary(string="Image")

    def action_view_setup_tool(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'SetupTool',
            'res_model': 'setup.sheet',
            'view_mode': 'form',
            'target': 'current',
        }

class SetupGallery(models.Model):
    _name = 'setup.gallery'
    _description = 'Setup Gallery'


    ImageGallery = fields.Binary(string="Image")
    name = fields.Char(string="Name", related='ToolSheet_id.ToolDescription')


    SetupTool_id = fields.Many2one('master.sheet', string='Tool')
    ToolSheet_id = fields.Many2one('tool.property', string='Tool')

    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name

    def action_view_gallery(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'SetupGallery',
            'res_model': 'setup.gallery',
            'view_mode': 'form',
            'target': 'current',
        }

    def action_delete_record(self):
        self.unlink()
        return True

class SetupCustomer(models.Model):
    _name = 'setup.customer'
    _description = 'Setup Gallery'

    name = fields.Char(string="Customer", required=True)

###########################Stores Historical Date##################################


class SetupHistory(models.Model):
    _name = 'setup.history'
    _description = 'Setup History'

    name = fields.Char(string="Name", required=True)

    DrawingNumber = fields.Char(string="Drawing Number")
    Revision = fields.Char(string="Revision")
    Material = fields.Char(string="Material")
    CNC_ProgramNumber = fields.Char(string="CNC Program #")
    CycleTime = fields.Char(string="Cycle Time")
    WorkOffset = fields.Char(string="Work Offset")
    WorkHolding = fields.Char(string="Work Holding")
    MountingFixture = fields.Char(string="Mounting Fixture")

    LessonLearntNotes = fields.Text(string="Lesson Learnt")
    ProgramModificationNotes = fields.Text(string="Any Porgram Modification?")
    Paths = fields.Binary(string="Path")

    SetupVerified = fields.Char(string="Setup Verified by")
    RecordVerified = fields.Char(string="Record Verified by")

    ProgramNumber = fields.Char(string="Program Number")
    CustomerPartNumber = fields.Char(string="Customer Part Number")
    ECL = fields.Char(string="ECL")

    SafetyEquipment = fields.Char(string="Safety Equipment")

    DateIssued = fields.Datetime(string="Date Issued")
    DateRevised = fields.Datetime(string="Date Revised")

    PartImage = fields.Image(string="Part Image")

    ControllerDocument = fields.Binary(string="Controller Document")
    ControllerDocument_filename = fields.Char(
        string="Controller Document filename",
    )


