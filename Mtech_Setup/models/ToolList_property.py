from odoo import models, fields, api

class Tool_Property(models.Model):
    _name = "tool.property"
    _description = "Tool Property"

    Tool_id = fields.Many2one('tool.type', string="Type", domain="[('ToolPart', '=', ToolPart)]")
    ToolNumber = fields.Char(string="Tool Number")
    ToolDescription = fields.Char(string="Tool Description")

    def _machineid_list(self):
        selection = []
        for j in range(100):
            a = 'MTL' + "{:03d}".format(j+1)
            selection.append((a, a))

        return selection

    ToolPart = fields.Char(string ='Tool Part', store = True)

    Supplier = fields.Char(string="Supplier")
    SelectUnits = fields.Selection([('Inches', 'inches'), ('Millimeter', 'millimeter')], string="Units", default="Inches")

    def _compute_display_name(self):
        for record in self:
           record.display_name = record.ToolNumber if record.ToolNumber else record.ToolDescription

    @api.depends('SelectUnits', 'Diameter')
    def CheckUnitForDiameter(self):
        for record in self:
            if record.Diameter:
                if record.SelectUnits == 'Millimeter':
                    record.adj_Diameter = record.Diameter / 25.4

                else:
                    record.adj_Diameter = record.Diameter
            else:
                record.adj_Diameter = 0

    @api.depends('SelectUnits', 'Length')
    def CheckUnitForLength(self):
        for record in self:
            if record.Length:
                if record.SelectUnits == 'Millimeter':
                    record.adj_Length = record.Length / 25.4
                else:
                    record.adj_Length = record.Length
            else:
                record.adj_Length = 0

    def SubmitAction(self):
        self.ensure_one()
        tree_view_id = self.env.ref("Mtech_Setup.tool_property_tree_view").id

        for record in self:
            print(record.ToolPart)
            if record.ToolPart == 'Drill':
                print("Hello")
                return {
                    "type": "ir.actions.act_window",
                    "name": "Tool",
                    "res_model": "tool.property",
                    "view_mode": "tree,form",
                    "views": [(tree_view_id, 'tree')],
                    "context": {'default_ToolPart': 'Drill'},
                    "domain": [('ToolPart', '=', 'Drill')],
                    "target": "current"
                }

            if record.ToolPart == 'OD':
                return {
                    "type": "ir.actions.act_window",
                    "name": "OD",
                    "res_model": "tool.property",
                    "view_mode": "tree,form",
                    "views": [(tree_view_id, 'tree')],
                    "context": {'default_ToolPart': 'OD'},
                    "domain": [('ToolPart', '=', 'OD')],
                    "target": "current"
                }

            if record.ToolPart == 'ID':
                return {
                    "type": "ir.actions.act_window",
                    "name": "ID",
                    "res_model": "tool.property",
                    "view_mode": "tree,form",
                    "views": [(tree_view_id, 'tree')],
                    "context": {'default_ToolPart': 'ID'},
                    "domain": [('ToolPart', '=', 'ID')],
                    "target": "current"
                }

            if record.ToolPart == 'Partoff':
                return {
                    "type": "ir.actions.act_window",
                    "name": "Partoff",
                    "res_model": "tool.property",
                    "view_mode": "tree,form",
                    "views": [(tree_view_id, 'tree')],
                    "context": {'default_ToolPart': 'Partoff'},
                    "domain": [('ToolPart', '=', 'Partoff')],
                    "target": "current"
                }

        return True

    Diameter = fields.Float(string="Diameter")
    adj_Diameter = fields.Float(string="Diameter", compute = "CheckUnitForDiameter", store = True)

    Length = fields.Float(string="Length")
    adj_Length = fields.Float(string="Length", compute = "CheckUnitForLength", store = True)

    Duplicate = fields.Integer(string="Count")
    Count = fields.Integer(string="Count")

    ImageGallery = fields.Binary(string="Image")


class Tool_Type(models.Model):
    _name = "tool.type"
    _description = "Tool type"


    ToolType = fields.Char(string="Tool Type")
    ToolPart = fields.Char(string="Tool Part")

    def _compute_display_name(self):
        for record in self:
           record.display_name = record.ToolType
