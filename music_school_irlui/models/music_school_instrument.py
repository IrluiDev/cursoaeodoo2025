from odoo import models, fields


class MusicSchoolInstrument(models.Model):
    _name = 'music.school.instrument'
    _description = 'Instruments'

    name = fields.Char(string="Name", required=True)
    family_id = fields.Many2one(
        comodel_name='music.school.instrument.family',
        string="Family",
        help="Family of the instrument"
    )
    # lo anterior sustituye el selection
    # family = fields.Selection(
    #     selection=[
    #         ('string', 'String'),
    #         ('wind', 'Wind'),
    #         ('percussion', 'Percussion'),
    #         ('keyboard', 'Keyboard'),
    #         ('electronic', 'Electronic'),
    #     ],
    #     string="Family",
    #     required=True,
    # )
    description = fields.Text(string="Description")
    last_maintenance_date = fields.Date(
        string="Last Maintenance Date",
        help="Date of the last maintenance performed on the instrument"
    )

    def instrument_maintenance(self):
        for record in self:
            record.last_maintenance_date = fields.Date.today()
    