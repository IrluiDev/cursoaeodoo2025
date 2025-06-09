from odoo import models, fields


class MusicSchoolInstrument(models.Model):
    _name = 'music.school.instrument'
    _description = 'Instruments'

    name = fields.Char(string="Name", required=True, translate=True)
    family_id = fields.Many2one(
        comodel_name='music.school.instrument.family',
        string="Family",
        help="Family of the instrument"
    )
    description = fields.Text(string="Description")
    last_maintenance_date = fields.Date(
        string="Last Maintenance Date",
        help="Date of the last maintenance performed on the instrument"
    )

    is_repaired = fields.Boolean(
        string="Is Repaired",
        compute='_compute_is_repaired',
        inverse='_set_is_repaired',

    )

    def _compute_is_repaired(self):
        for record in self:
            record.is_repaired = bool(record.last_maintenance_date)
            # if record.last_maintenance_date:
            #     record.is_repaired = True
            # else:
            #     record.is_repaired = False
    
    def _set_is_repaired(self):
        for record in self:
            if record.is_repaired:
                record.last_maintenance_date = fields.Date.today()
            else:
                record.last_maintenance_date = False

    def instrument_maintenance(self):
        for record in self:
            record.last_maintenance_date = fields.Date.today()