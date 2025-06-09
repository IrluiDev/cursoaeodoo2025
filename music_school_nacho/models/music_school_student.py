from odoo import models, fields, api


class MusicSchoolStudent(models.Model):
    _name = 'music.school.student'
    _description = 'Students'

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Name", required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Partner",
        help="Partner associated with this student"
    )
    email = fields.Char(string="Email", related="partner_id.email", store=True, readonly=False)
    phone = fields.Char(string="Phone", related="partner_id.phone", store=True, readonly=False)
    birthdate = fields.Date(string="Birthdate")
    age = fields.Integer(string="Age", compute='_compute_age', store=True)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Responsible",
        help="Responsible user for this student",
        copy=False
    )
    notes = fields.Html(
        string="Notes",
        help="Additional notes about the student",
        copy=False
    )

    reference = fields.Char(
        string="Reference",
    )
    
    @api.depends('birthdate')
    def _compute_age(self):
        for record in self:
            if record.birthdate:
                today = fields.Date.today()
                age = today.year - record.birthdate.year
                record.age = age
            else:
                record.age = 0

    def generate_reference(self):
        for record in self:
            record.reference = f"ESC-{record.id}{record.name}"