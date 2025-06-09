from odoo import models, fields, api


class MusicSchoolStudent(models.Model):
    _name = 'music.school.student'
    _description = 'Students'

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Name", required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Partner",
        help="Partner associated with the student"
    )
    email = fields.Char(
        string="Email",
        help="Email address of the student",
        related='partner_id.email',
        readonly=False,
        store=True)
    phone = fields.Char(
        string="Phone",
        help="Phone number of the student",
        related='partner_id.phone',
        readonly=False,
        store=True
        )
    birthdate = fields.Date(string="Birthdate")
    age = fields.Integer(
        string="Age",
        compute='_compute_age',
        store=True,
        help="Age of the student, computed from birthdate")
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Responsible",
        help="Responsible user for this student"
    )
    notes = fields.Html(
        string="Notes",
        help="Additional notes about the student"
    )

    @api.depends('birthdate')
    def _compute_age(self):
        for student in self:
            if student.birthdate:
                today = fields.Date.today()
                age = today.year - student.birthdate.year
                if (today.month, today.day) < (student.birthdate.month, student.birthdate.day):
                    age -= 1
                student.age = age
            else:
                student.age = 0
    
    @api.onchange('partner_id')
    def _onchange_email(self):
        if self.partner_id:
            self.email = self.partner_id.email
            self.phone = self.partner_id.phone
        else:
            self.email = ''
            self.phone = ''


            
    
    
